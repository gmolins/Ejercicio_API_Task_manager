from sqlmodel import SQLModel, Field
from typing import Optional

class StatusBase(SQLModel):
    name: str = Field(unique=True)
    color: Optional[str]

class Status(StatusBase, table=True):
    id: int = Field(primary_key=True)

