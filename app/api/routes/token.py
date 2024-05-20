import datetime
from datetime import timedelta
from fastapi import APIRouter, HTTPException


from typing import Annotated

from jose import JWTError
from pydantic import BaseModel

from app.api.db.sqlite_database import db_dependencies
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import jwt
from starlette import status


from app.api.models.models import Users
from app.api.routes.auth import pwd_context
from app.config.settings import settings

router = APIRouter()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: str, token_expiration_time: timedelta
) -> str:
    """
    Creates an access token (JWT) for a user with a specified expiration time.

    Args:
        username (str): The username of the user.
        user_id (str): The unique identifier of the user.
        token_expiration_time (timedelta): The time duration after which
        the token will expire.

    Returns:
        str: The encoded access token.
    """
    # Set the payload for the token
    payload = {
        "sub": username,  # Subject (the user's username)
        "id": user_id,  # User's unique identifier
    }

    # Calculate the expiration time for the token
    expiration_time = datetime.datetime.utcnow() + token_expiration_time
    payload["exp"] = expiration_time  # Add the expiration time to the payload

    # Encode the payload into a JWT token
    access_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return access_token


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependencies,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        token_expiration_time=timedelta(minutes=20),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
