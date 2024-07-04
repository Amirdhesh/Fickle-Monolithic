from typing import Annotated
from fastapi import APIRouter, Cookie, Depends
from fastapi_limiter.depends import RateLimiter
from app.core.security import user_credentials
from app.core.db_init import async_session
from fastapi_pagination import Page, paginate
from app.schema.solution import solutionCreate, message, solutionUpdate, solutionRead
from app.crud.solution import (
    contribute,
    delete,
    edit,
    display_solution,
)

route = APIRouter()


@route.post("/{problemstatement_id}/post-solution", status_code=200,dependencies=[Depends(RateLimiter(times=1,seconds=5))])
async def post_solution(
    *,
    session: async_session,
    problemstatement_id: str,
    solution: solutionCreate,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await contribute(
        session=session,
        problemstatement_id=problemstatement_id,
        solution=solution,
        user_id=data.id,
    )
    return message(message="Posted successfully.")


@route.delete("/{problemstatement_id}/delete-solution/{solution_id}", status_code=204,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def delete_solution(
    *,
    session: async_session,
    problemstatement_id: str,
    solution_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await delete(
        session=session,
        problemstatement_id=problemstatement_id,
        user_id=data.id,
        solution_id=solution_id,
    )
    return message(message="Posted successfully.")


@route.patch("/{problemstatement_id}/edit-solution/{solution_id}", status_code=200,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def edit_problemstatement(
    *,
    session: async_session,
    problemstatement_id: str,
    solution_id: str,
    solution: solutionUpdate,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await edit(
        session=session,
        problemstatement_id=problemstatement_id,
        solution_id=solution_id,
        solution=solution,
        user_id=data.id,
    )
    return message(message="Edited successfully.")


@route.get(
    "/{problemstatement_id}/display_solutions",
    status_code=200,
    response_model=Page[solutionRead],
    dependencies=[Depends(RateLimiter(times=1,seconds=10))]
)
async def problemstatement_solutions(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    await user_credentials(token=fickel_token)
    solutions = await display_solution(
        session=session, problemstatement_id=problemstatement_id
    )
    return paginate(solutions)
