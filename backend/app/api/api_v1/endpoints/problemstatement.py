
from typing import Annotated
from fastapi import APIRouter, Cookie, HTTPException
from app.core.security import user_credentials
from app.core.db_init import async_session
from app.schema.problemstatement import problemstatementCreate,message,problemstatementEdit
from app.crud.problemstatment import add_problemstatement, problemstatement_delete,problemstatement_edit
route = APIRouter()


@route.post("/post-problemstatement",status_code=201)
async def post_problemstatement(*,session:async_session,fickel_token:Annotated[str | None, Cookie()]=None,problemstatement:problemstatementCreate):
    data = await user_credentials(token=fickel_token)
    await add_problemstatement(session=session,problemstatement=problemstatement,user_id=data.id)
    return message(
        message="Problemstatement added successfully."
    )


@route.delete("/delete-problemstatement/{problemstatement_id}",status_code=204)
async def delete_problemstatement(*,session:async_session,problemstatement_id:str,fickel_token:Annotated[str | None,Cookie()]=None):
    data = await user_credentials(token=fickel_token)
    await problemstatement_delete(session=session, problemstatement_id=problemstatement_id, user_id=data.id)
    return message(
        message="Successfully deleted."
    )


@route.patch("/edit-problemstatement/{problemstatement_id}",status_code=201)
async def edit_problemstatement(*,session:async_session,problemstatement_id:str,problemstatement:problemstatementEdit,fickel_token:Annotated[str | None,Cookie()]=None):
    data = await user_credentials(token=fickel_token)
    await problemstatement_edit(session=session,problemstatement_id=problemstatement_id,problemstatement=problemstatement.problemstatment,user_id=data.id)
    return message(
        message="Edited successfully."
    )
