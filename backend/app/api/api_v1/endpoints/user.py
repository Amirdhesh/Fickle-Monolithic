from typing import Annotated,Union
from fastapi import Cookie,APIRouter, Response, HTTPException
from app.schema.user import userCreate,message
from app.core.db_init import async_session
from app.schema.user import userCreate,userRead,TokenResponse,changePassword,userUpdate
from app.crud.user import add_user,update_user,change_password
from app.core.security import create_token,user_credentials
from app.core.settings import settings

route = APIRouter()


@route.post("/register",status_code=201,response_model=message)
async def create_user(session: async_session, user_in: userCreate,response: Response): 
    user: userRead = await add_user(session=session,user_create=user_in)
    token = await create_token(id=user.id , email=user.id)
    response.set_cookie(key = "fickel_token",value=token,expires=(settings.JWT_EXPIRY_TIME*3600))
    return message(
        message="User has been successfully added."
        )


@route.patch("/change_password")
async def Password_change(session:async_session,password:changePassword,token:str):
    data =await user_credentials(token=token)
    if password.new_password != password.reenter_password:
        raise HTTPException(
            status_code=400,
            detail="Both are different passwords."
        )
    await change_password(session=session,password=password,id = data.id)
    return message(
        message="User updated successfully."
    )