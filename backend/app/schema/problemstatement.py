from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import date

class problemstatmentBase(SQLModel):
    Name : str = Field(index=True,unique=True)
    problemstatment : str = Field(nullable=False)
    created_date : date = Field(default=date.today())
    user_id : Optional[int] = Field(default=None,foreign_key="users.id")

class problemstatementCreate(problemstatmentBase):
    pass

class problemstatementRead(problemstatmentBase):
    id:int
    likes_count :int

class problemstatementUpdate(SQLModel):
    Name : Optional[str] 
    problemstatment :Optional[str] 
    created_date : Optional[date]
