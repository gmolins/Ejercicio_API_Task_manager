from sqlmodel import SQLModel, Field
from typing import Optional

from models.todo import TodoList

class StatusBase(SQLModel):
    name: str = Field(unique=True)
    color: Optional[str]

class Status(StatusBase, table=True):
    id: int = Field(primary_key=True)
    todo_list_id: TodoList = Field(foreign_key="todo_lists.id")

