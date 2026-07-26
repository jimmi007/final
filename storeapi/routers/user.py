import logging
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Request, status, Form, Depends
from storeapi.database import database, user_table
from storeapi.models.user import UserIn
from storeapi.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    get_subject_for_token_type,
    get_user,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn, request: Request):
    logger.info("REGISTER endpoint called")
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )
    # λάθος το getuser
    # το httpexception εχεί status_code και detail
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)
    # εγγραφή για πρόσθεση mail passwoed
    logger.debug(query)

    await database.execute(query)
    return {
        "detail": "User created. Please confirm your email.",
        "confirmation_url": request.url_for(
            "confirm_email", token=create_confirmation_token(user.email)
        ),
    }


@router.post("/token")
# η ιστοσελίδα που ανοίγει
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username,form_data.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_for_token_type(token, "confirmation")
    query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )
    # το query είναι υποπίνακας φιλτραρισμένος βάσει το confirmed true,βρίσκει  βάσει email
    logger.debug(query)

    await database.execute(query)
    return {"detail": "User confirmed"}


# εκτελεί η database και επιστρέφει json
