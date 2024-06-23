from sqlmodel import SQLModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schema.problemstatement import problemstatementProfile
from app.schema.solution import solutionProfile


class userBase(SQLModel):
    Name: str = Field(index=True)
    email: str = Field(unique=True)
    email_verified: bool = Field(default=False)
    password: str
    about: Optional[str] = Field(default=None)


class userCreate(userBase):
    pass


class userRead(SQLModel):
    id: UUID
    email_verified: bool
    about: str
    name: str
    created_at: datetime


class userUpdate(SQLModel):
    Name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    about: Optional[str]


class userLogin(SQLModel):
    email: str
    password: str


class message(SQLModel):
    message: str


class changePassword(SQLModel):
    new_password: str
    reenter_password: str


class TokenResponse(SQLModel):
    id: UUID
    email: str


class loginUser(SQLModel):
    email: str
    password: str


class userProfile(SQLModel):
    user: userRead
    problemstatements: List[problemstatementProfile]
    solutions: List[solutionProfile]
