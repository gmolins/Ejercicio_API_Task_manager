from datetime import datetime, date
from sqlmodel import Enum, SQLModel, Field
from typing import Optional
from pydantic import EmailStr

from app.models.todo import TodoList

class StatusEnum(str, Enum):
    wip = "WIP"
    completado = "Completado"
    blocker = "Blocker"

class StatusBase(SQLModel):
    name: StatusEnum
    email: EmailStr = Field(unique=True)
    role: str = Field(default="user")
    color: Optional[str]

class Status(StatusBase, table=True):
    id: int = Field(primary_key=True)
    todo_list_id: TodoList = Field(foreign_key="todo_lists.id")

