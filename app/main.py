from fastapi import FastAPI

from app.api.models import models
from app.api.db.sqlite_database import engine

from app.api.routes import router as api_router

app = FastAPI()

models.Base

app.include_router(api_router)


models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
