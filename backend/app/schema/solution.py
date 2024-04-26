from sqlmodel import SQLModel, Field
from typing import Optional
from app.schema import baseUUID


class solutionBase(SQLModel):
    solution: str = Field(nullable=False)
    solution_link: Optional[str] = Field(default=None)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    problemstatment_id: Optional[int] = Field(
        default=None, foreign_key="problemstatement.id"
    )


class solutionCreate(solutionBase):
    pass


class solutionRead(baseUUID, solutionBase):
    pass


class solutionUpdate(SQLModel):
    solution: Optional[str]
    solution_link: Optional[str]
