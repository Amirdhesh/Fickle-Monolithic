from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from app.schema.baseuuid import baseUUID
from uuid import UUID
from datetime import datetime


class problemstatmentBase(SQLModel):
    Name: str = Field(index=True, unique=True)
    problemstatment: str = Field(nullable=False)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")


class problemstatementCreate(SQLModel):
    Name: str = Field(index=True, unique=True)
    problemstatment: str = Field(nullable=False)


class problemstatementRead(baseUUID, problemstatmentBase):
    likes: int


class problemstatementUpdate(SQLModel):
    Name: Optional[str]
    problemstatment: Optional[str]
    created_date: Optional[date]


class message(SQLModel):
    message: str


class problemstatementEdit(SQLModel):
    problemstatment: str


class problemstatementwishlist(SQLModel):
    id: int
    problemstatement_id: UUID
    Name: str
    created_at: datetime
    problemstatement: str


class problemstatementProfile(baseUUID, SQLModel):
    Name: str
    problemstatement: str
