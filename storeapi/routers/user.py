import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
import sqlalchemy
from fastapi.security import OAuth2PasswordRequestForm
from storeapi.security import get_current_user
from storeapi.database import database, user_table
from storeapi.models.user import Token, UserIn
from storeapi.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    get_subject_for_token_type,
)
from storeapi.tasks import send_simple_email


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserIn,
    background_tasks: BackgroundTasks,
    request: Request,
):
    print("1. Register started")

    existing_user = await database.fetch_one(
        user_table.select().where(
            user_table.c.email == user.email
        )
    )
    print("2. Existing user checked")

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    hashed_password = get_password_hash(user.password)
    print("3. Password hashed")

    query = user_table.insert().values(
        email=user.email,
        password=hashed_password,
        confirmed=False,
    )

    user_id = await database.execute(query)
    print("4. User inserted")

    confirmation_token = create_confirmation_token(
        user.email
    )
    print("5. Token created")

    confirmation_url = request.url_for(
        "confirm_user",
        token=confirmation_token,
    )
    print("6. URL created")

    background_tasks.add_task(
        send_simple_email,
        user.email,
        "Confirm your account",
        f"Confirm your account here: {confirmation_url}",
    )
    print("7. Email task added")

    return {
        "detail": "User created. Please confirm your email.",
        "id": user_id,
    }

@router.post(
    "/token",
    response_model=Token,
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
):
    user = await authenticate_user(
        form_data.username,
        form_data.password,
    )

    access_token = create_access_token(
        user.email
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.delete("/user", status_code=status.HTTP_200_OK)
async def delete_user(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    background_tasks: BackgroundTasks,
):
    logger.info(
        "Deleting user",
        extra={"email": current_user.email},
    )

    # Posts που ανήκουν στον χρήστη
    user_post_ids = (
        sqlalchemy.select(post_table.c.id)
        .where(post_table.c.user_id == current_user.id)
    )

    # Likes που έκανε ο χρήστης ή αφορούν δικά του posts
    await database.execute(
        like_table.delete().where(
            sqlalchemy.or_(
                like_table.c.user_id == current_user.id,
                like_table.c.post_id.in_(user_post_ids),
            )
        )
    )

    # Comments που έκανε ο χρήστης ή αφορούν δικά του posts
    await database.execute(
        comment_table.delete().where(
            sqlalchemy.or_(
                comment_table.c.user_id == current_user.id,
                comment_table.c.post_id.in_(user_post_ids),
            )
        )
    )

    # Διαγραφή των posts του
    await database.execute(
        post_table.delete().where(
            post_table.c.user_id == current_user.id
        )
    )

    # Διαγραφή χρήστη
    await database.execute(
        user_table.delete().where(
            user_table.c.id == current_user.id
        )
    )

    # Email ενημέρωσης
    background_tasks.add_task(
        send_simple_email,
        current_user.email,
        "Account deleted",
        "Your account has been deleted successfully.",
    )

    return {
        "message": "User deleted successfully"
    }