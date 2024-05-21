from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from app.api.db.sqlite_database import db_dependencies
from starlette import status
from app.api.models.models import Todos, Users
from app.api.routes.token import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter()


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependencies, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Authorized",
        )
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependencies, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" User not Authorized",
        )
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()

    return {"message": "Todo deleted successfully"}


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependencies, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" User not Authorized",
        )
    return db.query(Users).all()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: user_dependency, db: db_dependencies, user_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" User not Authorized",
        )

    user_model = db.query(Users).filter(Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete todos associated with the user
    todos = db.query(Todos).filter(Todos.owner_id == user_id).all()
    for todo in todos:
        db.delete(todo)

    db.delete(user_model)
    db.commit()

    return {"message": "User deleted successfully"}
