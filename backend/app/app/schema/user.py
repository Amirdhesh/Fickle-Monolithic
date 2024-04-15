from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import date

class userBase(SQLModel):
    Name : str = Field(index=True)
    email:str = Field(unique=True)
    password:str
    about:Optional[str] = Field(default=None)
    date_joined : date = Field(default=date.today())

class userCreate(userBase):
    pass

class userRead(userBase):
    id:int

class userUpdate(SQLModel):
    Name : Optional[str]
    email:Optional[str]
    password:str
    about:Optional[str]


class userLogin(SQLModel):
    email:str
    password:str

