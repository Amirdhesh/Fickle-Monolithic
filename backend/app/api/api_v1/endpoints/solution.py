from typing import Annotated
from fastapi import APIRouter, HTTPException, Cookie
from app.core.security import user_credentials
from app.core.db_init import async_session
from app.schema.solution import solutionCreate, message, solutionUpdate, solutionRead
from app.crud.solution import (
    add_solution,
    solution_delete,
    update_solution,
    display_solution,
)

route = APIRouter()


@route.post("/{problemstatement_id}/post-solution", status_code=200)
async def post_solution(
    *,
    session: async_session,
    problemstatement_id: str,
    solution: solutionCreate,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    await add_solution(
        session=session,
        problemstatement_id=problemstatement_id,
        solution=solution,
        user_id=data.id,
    )
    return message(message="Posted successfully.")


@route.delete("/{problemstatement_id}/delete-solution/{solution_id}", status_code=204)
async def delete_solution(
    *,
    session: async_session,
    problemstatement_id: str,
    solution_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    await solution_delete(
        session=session,
        problemstatement_id=problemstatement_id,
        user_id=data.id,
        solution_id=solution_id,
    )
    return message(message="Posted successfully.")


@route.patch("/{problemstatement_id}/edit-solution/{solution_id}", status_code=200)
async def edit_problemstatement(
    *,
    session: async_session,
    problemstatement_id: str,
    solution_id: str,
    solution: solutionUpdate,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    await update_solution(
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
    response_model=list[solutionRead],
)
async def problemstatement_solutions(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    await user_credentials(token=fickel_token)
    solutions = await display_solution(
        session=session, problemstatement_id=problemstatement_id
    )
    return solutions
