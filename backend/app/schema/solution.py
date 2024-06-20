from sqlmodel import SQLModel, Field
from typing import Optional
from app.schema.baseuuid import baseUUID
from uuid import UUID
from datetime import datetime


class solutionBase(SQLModel):
    solution: str = Field(nullable=False)
    solution_link: Optional[str] = Field(default=None)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    problemstatment_id: Optional[UUID] = Field(
        default=None, foreign_key="problemstatement.id"
    )


class solutionCreate(SQLModel):
    solution: str
    solution_link: Optional[str]


class solutionRead(baseUUID, SQLModel):
    id: UUID
    solution: Optional[str]
    solution_link: Optional[str]


class solutionUpdate(SQLModel):
    solution: Optional[str]
    solution_link: Optional[str]


class message(SQLModel):
    message: str
