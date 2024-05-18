from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from app.api.db.sqlite_database import db_dependencies
from starlette import status
from app.api.models.models import Todos

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependencies):
    return db.query(Todos).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependencies, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(request: TodoRequest, db: db_dependencies):
    todo = Todos(**request.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    request: TodoRequest,
    db: db_dependencies,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = request.title
    todo_model.description = request.description
    todo_model.priority = request.priority
    todo_model.completed = request.completed
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependencies, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()

    return {"message": "Todo deleted successfully"}
