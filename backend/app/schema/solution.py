from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import date


class solutionBase(SQLModel):
    solution : str = Field(nullable=False)
    solution_link : Optional[str] = Field(default=None)
    date_submitted : date = Field(default=date.today())
    user_id : Optional[int] = Field(default=None,foreign_key="user.id")
    problemstatment_id : Optional[int] = Field(default=None,foreign_key="problemstatment.id")

class solutionCreate(solutionBase):
    pass


class solutionRead(solutionBase):
    id:int


class solutionUpdate(SQLModel):
    solution : Optional[str]
    solution_link : Optional[str]
