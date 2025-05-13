from datetime import datetime, date
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

from app.models.status import Status
from app.models.todo import TodoList

class TaskBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    role: str = Field(default="user")
    title: str
    description: Optional[str]
    due_date: Optional[date]

class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)
    is_completed: bool
    created_at: datetime
    todo_list_id: TodoList = Field(foreign_key="todo_lists.id")
    status_id: Status = Field(foreign_key="status.id")

