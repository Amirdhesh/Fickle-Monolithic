from typing import Annotated, List
from fastapi import APIRouter, Cookie, Depends
from fastapi_limiter.depends import RateLimiter
from app.core.security import user_credentials
from app.core.db_init import async_session
from app.schema.problemstatement import (
    problemstatementCreate,
    message,
    problemstatementEdit,
    problemstatementRead,
    problemstatementSearch,
)
from app.crud.problemstatment import (
    post,
    delete,
    edit,
    display_problemstatements,
    like,
    search,
)


route = APIRouter()


@route.post("/post-problemstatement", status_code=201,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def post_problemstatement(
    *,
    session: async_session,
    fickel_token: Annotated[str | None, Cookie()] = None,
    problemstatement: problemstatementCreate,
):
    data = await user_credentials(token=fickel_token)
    await post(session=session, problemstatement=problemstatement, user_id=data.id)
    return message(message="Problemstatement added successfully.")


@route.delete("/delete-problemstatement/{problemstatement_id}", status_code=204,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def delete_problemstatement(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)

    await delete(
        session=session, problemstatement_id=problemstatement_id, user_id=data.id
    )
    return message(message="Successfully deleted.")


@route.patch("/edit-problemstatement/{problemstatement_id}", status_code=201,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def edit_problemstatement(
    *,
    session: async_session,
    problemstatement_id: str,
    problemstatement: problemstatementEdit,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await edit(
        session=session,
        problemstatement_id=problemstatement_id,
        problemstatement=problemstatement.problemstatment,
        user_id=data.id,
    )
    return message(message="Edited successfully.")


@route.post("/like/{problemstatement_id}", status_code=201,dependencies=[Depends(RateLimiter(times=1,seconds=10))])
async def like_problemstatement(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await like(
        session=session, user_id=data.id, problemstatement_id=problemstatement_id
    )
    return message(message="liked")


@route.get(
    "/display_problemstatements",
    status_code=200,
    response_model=List[problemstatementRead],
    dependencies=[Depends(RateLimiter(times=1,seconds=10))]
)
async def display_problemstatment(
    *, session: async_session, fickel_token: Annotated[str | None, Cookie()] = None
):
    await user_credentials(token=fickel_token)
    problemstatements = await display_problemstatements(session=session)
    return problemstatements


@route.get("/search", status_code=200, response_model=List[problemstatementSearch],dependencies=[Depends(RateLimiter(times=1,seconds=5))])
async def search_problemstatement(
    *,
    session: async_session,
    problemstatement_name: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    await user_credentials(token=fickel_token)
    problemstatements = await search(
        session=session, problemstatement_name=problemstatement_name
    )
    return problemstatements
