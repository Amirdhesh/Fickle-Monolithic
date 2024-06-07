from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from app.schema.baseuuid import baseUUID
from uuid import UUID


class problemstatmentBase(SQLModel):
    Name: str = Field(index=True, unique=True)
    problemstatment: str = Field(nullable=False)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")


class problemstatementCreate(SQLModel):
    Name: str = Field(index=True, unique=True)
    problemstatment: str = Field(nullable=False)


class problemstatementRead(baseUUID, problemstatmentBase):
    likes_count: int


class problemstatementUpdate(SQLModel):
    Name: Optional[str]
    problemstatment: Optional[str]
    created_date: Optional[date]


class message(SQLModel):
    message: str

class problemstatementEdit(SQLModel):
    problemstatment:str