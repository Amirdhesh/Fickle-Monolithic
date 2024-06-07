from fastapi import HTTPException
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from app.schema.problemstatement import problemstatementCreate,problemstatementEdit
from app.model import Problemstatement,Users

async def add_problemstatement(*,session:AsyncSession,problemstatement:problemstatementCreate,user_id:UUID):
    try:
        problemstatement = Problemstatement.model_validate(problemstatement,update={"user_id":user_id})
        session.add(problemstatement)
        await session.commit()
        await session.refresh(problemstatement)
        return problemstatement
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Unable to add. {e}"
        )
    

async def problemstatement_delete(*,session:AsyncSession,problemstatement_id:UUID,user_id:UUID):
    try:
        statement = select(Problemstatement).where(
            (Problemstatement.id == problemstatement_id) &
            (Problemstatement.user_id == user_id)
        )
        problemstatement = (await session.exec(statement=statement)).one_or_none()
        await session.delete(problemstatement)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail="Unable to delete."
        )
    

async def problemstatement_edit(*,session:AsyncSession,problemstatement:str,problemstatement_id:UUID,user_id:UUID):
    try:
        statement = select(Problemstatement).where(
            (Problemstatement.id == problemstatement_id) &
            (Problemstatement.user_id == user_id)
        )
        response = (await session.exec(statement=statement)).one_or_none()
        response.problemstatment = problemstatement
        session.add(response)
        await session.commit()
        await session.refresh(response)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Not Found."
        )


async def verify_problemstatment(*,session:AsyncSession,problemstatement_id:UUID):
    statement = select(Problemstatement).where(Problemstatement.id == problemstatement_id)
    response = (await session.exec(statement=statement)).one_or_none()
    return response