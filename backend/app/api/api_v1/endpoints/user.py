from fastapi import APIRouter, Response, Cookie
from app.schema.user import userCreate
from app.core.db_init import async_session
from app.schema.user import userCreate,userRead
from app.crud.user import add_user
from app.core.security import create_token


route = APIRouter()


@route.post("/register")
async def create_user(session: async_session, user_in: userCreate,response: Response): 
    user: userRead = await add_user(session=session,user_create=user_in)
    token = create_token(id=user.id , email=user.id)
    response.set_cookie(key = "fickel_token",value=token)
    return {"User successfully added."}