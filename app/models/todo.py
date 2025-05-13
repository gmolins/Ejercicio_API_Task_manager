from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
from app.models.user import User
from app.models.task import Task

class TodoBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    role: str = Field(default="user")
    title: str
    description: Optional[str] = None

class TodoList(TodoBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    owner_id: User = Field(foreign_key="users.id")
    tasks: list[Task] = Field(foreign_key="tasks.id")