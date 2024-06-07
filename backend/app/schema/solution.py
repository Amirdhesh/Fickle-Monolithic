from sqlmodel import SQLModel, Field
from typing import Optional
from app.schema.baseuuid import baseUUID
from uuid import UUID


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


class solutionRead(baseUUID, solutionBase):
    pass


class solutionUpdate(SQLModel):
    solution: Optional[str]
    solution_link: Optional[str]


class message(SQLModel):
    message: str
