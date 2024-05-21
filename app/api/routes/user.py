from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.api.db.sqlite_database import db_dependencies
from starlette import status
from app.api.models.models import Users
from app.api.routes.token import get_current_user
from app.api.routes.auth import pwd_context

user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependencies, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return db.query(Users).filter(Users.id == user.get("id")).first()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user: user_dependency,
    user_verification: UserVerification,
    db: db_dependencies,
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not pwd_context.verify(
        user_verification.password,
        user_model.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Error verifying password",
        )

    user_model.hashed_password = pwd_context.hash(
        user_verification.new_password,
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model
