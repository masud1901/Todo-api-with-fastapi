from fastapi import APIRouter
from pydantic import BaseModel
from app.api.models.models import Users
from passlib.context import CryptContext
from app.api.db.sqlite_database import db_dependencies
from starlette import status


router = APIRouter()

pwd_context = CryptContext(schemes=["argon2"])


@router.get("/")
async def read_all(db: db_dependencies):
    return db.query(Users).all()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    db: db_dependencies,
):
    create_user = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=pwd_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user)
    db.commit()
    return create_user
