from uuid import UUID
from sqlmodel import select
from app.model import Solution
from fastapi import HTTPException
from app.schema.solution import solutionCreate, solutionUpdate
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.crud.problemstatment import verify_problemstatment


async def add_solution(
    *,
    session: AsyncSession,
    problemstatement_id: UUID,
    user_id: UUID,
    solution: solutionCreate,
):
    try:
        problemstatement_exist = await verify_problemstatment(
            session=session, problemstatement_id=problemstatement_id
        )
        if problemstatement_exist is None:
            raise HTTPException(status_code=404, detail="Not problemstatement found.")
        solution = Solution.model_validate(
            solution,
            update={"problemstatment_id": problemstatement_id, "user_id": user_id},
        )
        session.add(solution)
        await session.commit()
        await session.refresh(solution)
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Unable to add.{e}")


async def solution_delete(
    *,
    session: AsyncSession,
    problemstatement_id: UUID,
    user_id: UUID,
    solution_id: UUID,
):
    try:
        statement = select(Solution).where(
            (Solution.id == solution_id)
            & (Solution.problemstatment_id == problemstatement_id)
            & (Solution.user_id == user_id)
        )
        solution = (await session.exec(statement=statement)).one_or_none()
        await session.delete(solution)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Not Found.")


async def update_solution(
    *,
    session: AsyncSession,
    problemstatement_id: UUID,
    user_id: UUID,
    solution_id: UUID,
    solution: solutionUpdate,
):
    try:
        statement = select(Solution).where(
            (Solution.id == solution_id)
            & (Solution.problemstatment_id == problemstatement_id)
            & (Solution.user_id == user_id)
        )
        response = (await session.exec(statement=statement)).one_or_none()
        update = solution.model_dump(exclude_unset=True)
        response.sqlmodel_update(update)
        session.add(response)
        await session.commit()
        await session.refresh(response)
    except Exception as e:
        raise HTTPException(status_code=409, detail="Unable to delete.")


async def display_solution(*, session: AsyncSession, problemstatement_id: UUID):
    statement = select(
        Solution.id,
        Solution.solution,
        Solution.solution_link,
        Solution.created_at,
        Solution.updated_at,
    ).where(Solution.problemstatment_id == problemstatement_id)
    solutions = (await session.exec(statement=statement)).all()

    if not solutions:
        raise HTTPException(status_code=404, detail="No solution found")
    return solutions
