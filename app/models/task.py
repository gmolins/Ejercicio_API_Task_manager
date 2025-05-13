from datetime import datetime, date
from sqlmodel import SQLModel, Field
from typing import Optional, List

from models.status import Status
from models.todo import TodoList

class TaskBase(SQLModel):
    title: str
    description: Optional[str]
    due_date: Optional[date]

class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)
    is_completed: bool
    created_at: datetime
    todo_list_id: TodoList = Field(foreign_key="todo_lists.id")
    status_id: Optional[Status] = Field(foreign_key="status.id")

