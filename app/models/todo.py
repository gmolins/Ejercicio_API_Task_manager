from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional, List
from models.user import User
from models.task import Task

class TodoBase(SQLModel):
    title: str
    description: Optional[str]

class TodoList(TodoBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    owner_id: User = Field(foreign_key="users.id")
    tasks: Optional[List[Task]] = Field(foreign_key="tasks.id")