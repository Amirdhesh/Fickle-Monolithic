from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from app.schema import baseUUID


class problemstatmentBase(SQLModel):
    Name: str = Field(index=True, unique=True)
    problemstatment: str = Field(nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class problemstatementCreate(problemstatmentBase):
    pass


class problemstatementRead(baseUUID, problemstatmentBase):
    likes_count: int


class problemstatementUpdate(SQLModel):
    Name: Optional[str]
    problemstatment: Optional[str]
    created_date: Optional[date]
