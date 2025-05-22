from sqlmodel import Relationship, SQLModel, Field
from typing import Optional

class StatusBase(SQLModel):
    name: str = Field(unique=True)
    color: Optional[str]

class Status(StatusBase, table=True):
    id: int = Field(default=None, primary_key=True)

    task: Optional["Task"] = Relationship(back_populates="status", cascade_delete=True) # type: ignore

