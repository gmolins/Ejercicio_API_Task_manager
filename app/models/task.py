from datetime import datetime, date
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional

class TaskBase(SQLModel):
    title: str
    description: Optional[str]
    due_date: Optional[date] = None

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    is_completed: bool
    created_at: datetime
    todolist_id: int = Field(default=None, foreign_key="todolist.id", ondelete="CASCADE")

class TaskCreate(TaskBase):
    todolist_id: int = Field(description="Todo-List ID cant be empty")

class TaskRead(TaskBase):
    id: int