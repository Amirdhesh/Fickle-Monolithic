from sqlmodel import SQLModel, Field
from typing import Optional
from app.schema import baseUUID


class userBase(SQLModel):
    Name: str = Field(index=True)
    email: str = Field(unique=True)
    password: str
    about: Optional[str] = Field(default=None)


class userCreate(userBase):
    pass


class userRead(baseUUID, userBase):
    pass


class userUpdate(SQLModel):
    Name: Optional[str]
    email: Optional[str]
    password: str
    about: Optional[str]


class userLogin(SQLModel):
    email: str
    password: str
