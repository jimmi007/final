import logging
from typing import Annotated

import sqlalchemy
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from storeapi.database import (
    comment_table,
    database,
    like_table,
    post_table,
    user_table,
)
from storeapi.models.user import Token, User, UserIn
from storeapi.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_current_user,
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
    logger.info(
        "Creating user",
        extra={"email": user.email},
    )

    existing_user = await database.fetch_one(
        user_table.select().where(
            user_table.c.email == user.email
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    hashed_password = get_password_hash(user.password)

    query = user_table.insert().values(
        email=user.email,
        password=hashed_password,
        confirmed=False,
    )

    user_id = await database.execute(query)

    confirmation_token = create_confirmation_token(
        user.email
    )

    confirmation_url = request.url_for(
        "confirm_user",
        token=confirmation_token,
    )

    background_tasks.add_task(
        send_simple_email,
        user.email,
        "Confirm your account",
        f"Confirm your account here: {confirmation_url}",
    )

    return {
        "detail": "User created. Please confirm your email.",
        "id": user_id,
    }


@router.get(
    "/confirm/{token}",
    name="confirm_user",
)
async def confirm_user(token: str):
    email = get_subject_for_token_type(
        token,
        "confirmation",
    )

    query = (
        user_table.update()
        .where(user_table.c.email == email)
        .values(confirmed=True)
    )

    await database.execute(query)

    return {
        "detail": "User confirmed",
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


@router.delete(
    "/user",
    status_code=status.HTTP_200_OK,
)
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

    user_post_ids = (
        sqlalchemy.select(post_table.c.id)
        .where(post_table.c.user_id == current_user.id)
    )

    await database.execute(
        like_table.delete().where(
            sqlalchemy.or_(
                like_table.c.user_id == current_user.id,
                like_table.c.post_id.in_(user_post_ids),
            )
        )
    )

    await database.execute(
        comment_table.delete().where(
            sqlalchemy.or_(
                comment_table.c.user_id == current_user.id,
                comment_table.c.post_id.in_(user_post_ids),
            )
        )
    )

    await database.execute(
        post_table.delete().where(
            post_table.c.user_id == current_user.id
        )
    )

    await database.execute(
        user_table.delete().where(
            user_table.c.id == current_user.id
        )
    )

    background_tasks.add_task(
        send_simple_email,
        current_user.email,
        "Account deleted",
        "Your account has been deleted successfully.",
    )

    return {
        "message": "User deleted successfully",
    }