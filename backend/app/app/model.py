from sqlmodel import SQLModel,Field,Relationship
from typing import List,Optional
from schema import problemstatmentBase
from schema import userBase
from schema import solutionBase



class users(userBase,table=True):
    id : Optional[int] = Field(default=None,primary_key=True)
    problemstatement : List['problemstatement'] = Relationship(back_populates="user")
    solution : List['solution'] = Relationship(back_populates="user")

class problemstatement(problemstatmentBase,table = True):
    id:Optional[int] = Field(default=None,primary_key=True)
    user : users = Relationship(back_populates="users")
    solution : List['solution'] = Relationship(back_populates="problemstatement")
    like : List['like'] = Relationship(back_populates="user")

class solution(solutionBase,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    user:users = Relationship(back_populates="solution")
    problemstatement : List['problemstatement'] = Relationship(back_populates="solution")
    like : List['like'] = Relationship(back_populates="problemstatement")


class like(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    user_id : Optional[int] = Field(default=None,foreign_key="user.id")
    problemstatement_id : Optional[int] = Field(default=None,foreign_key="problemstatement.id")
    user:users = Relationship(back_populates="like")
    problemstatement : 'problemstatement' = Relationship(back_populates="like")


class wishlist(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    user_id : Optional[int] = Field(default=None,foreign_key="user.id")
    problemstatement_id : Optional[int] = Field(default=None,foreign_key="problemstatement.id")

