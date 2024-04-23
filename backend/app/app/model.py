from typing import List,Optional
from sqlmodel import SQLModel,Field,Relationship
from schema import problemstatmentBase,userBase,solutionBase



class Users(userBase,table=True):
    id : Optional[int] = Field(default=None,primary_key=True)
    problemstatement : List['Problemstatement'] = Relationship(back_populates="user")
    solution : List['Solution'] = Relationship(back_populates="user")

class Problemstatement(problemstatmentBase,table = True):
    id:Optional[int] = Field(default=None,primary_key=True)
    user : Users = Relationship(back_populates="problemstatement")
    solution : List['Solution'] = Relationship(back_populates="problemstatement")
    like : List['Like'] = Relationship(back_populates="problemstatement")

class Solution(solutionBase,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    user:Users = Relationship(back_populates="solution")
    problemstatement : List['Problemstatement'] = Relationship(back_populates="solution")


class Like(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    user_id : Optional[int] = Field(default=None,foreign_key="users.id")
    problemstatement_id : Optional[int] = Field(default=None,foreign_key="problemstatement.id")
    user:Users = Relationship(back_populates="like")
    problemstatement : 'Problemstatement' = Relationship(back_populates="like")


class Wishlist(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    user_id : Optional[int] = Field(default=None,foreign_key="user.id")
    problemstatement_id : Optional[int] = Field(default=None,foreign_key="problemstatement.id")

