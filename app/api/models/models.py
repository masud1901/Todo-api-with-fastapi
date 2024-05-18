from app.api.db.sqlite_database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
