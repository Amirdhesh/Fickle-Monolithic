from fastapi import HTTPException
from uuid import UUID
from sqlmodel import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schema.problemstatement import problemstatementCreate
from app.model import Problemstatement, Like, Wishlist
from sqlalchemy import delete


async def add_problemstatement(
    *, session: AsyncSession, problemstatement: problemstatementCreate, user_id: UUID
):
    try:
        problemstatement = Problemstatement.model_validate(
            problemstatement, update={"user_id": user_id}
        )
        session.add(problemstatement)
        await session.commit()
        await session.refresh(problemstatement)
        return problemstatement
    except Exception:
        raise HTTPException(status_code=409, detail="Unable to add.")


async def problemstatement_delete(
    *, session: AsyncSession, problemstatement_id: UUID, user_id: UUID
):
    try:
        statement = select(Problemstatement).where(
            (Problemstatement.id == problemstatement_id)
            & (Problemstatement.user_id == user_id)
        )
        problemstatement = (await session.exec(statement=statement)).one_or_none()
        await session.delete(problemstatement)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=409, detail="Unable to delete.")


async def problemstatement_edit(
    *,
    session: AsyncSession,
    problemstatement: str,
    problemstatement_id: UUID,
    user_id: UUID,
):
    try:

        statement = select(Problemstatement).where(
            (Problemstatement.id == problemstatement_id)
            & (Problemstatement.user_id == user_id)
        )
        response = (await session.exec(statement=statement)).one_or_none()
        response.problemstatment = problemstatement
        session.add(response)
        await session.commit()
        await session.refresh(response)
    except Exception:
        raise HTTPException(status_code=404, detail="Not Found.")


async def verify_problemstatment(*, session: AsyncSession, problemstatement_id: UUID):
    statement = select(Problemstatement).where(
        Problemstatement.id == problemstatement_id
    )
    response = (await session.exec(statement=statement)).one_or_none()
    return response


async def like(*, session: AsyncSession, problemstatement_id: UUID, user_id: UUID):
    statement = select(Like).where(
        (Like.user_id == user_id) & (Like.problemstatement_id == problemstatement_id)
    )
    already_liked = (await session.exec(statement=statement)).one_or_none()
    if already_liked:
        raise HTTPException(status_code=409, detail="Already Liked")
    like = Like(user_id=user_id, problemstatement_id=problemstatement_id)
    session.add(like)
    await session.commit()
    await session.refresh(like)
    return like


async def display_problemstatements(*, session: AsyncSession):
    statement = (
        select(Problemstatement, func.coalesce(func.count(Like.id), 0).label("likes"))
        .outerjoin(Like,Problemstatement.id == Like.problemstatement_id)
        .group_by(Problemstatement.id)
    )
    rows = (await session.exec(statement=statement)).all()
    response = [
        {
            "id": row[0].id,
            "user_id": row[0].user_id,
            "created_at": row[0].created_at,
            "Name": row[0].Name,
            "problemstatment": row[0].problemstatment,
            "likes": row[1],
        }
        for row in rows
    ]
    return response


async def add_problemstatement_to_wishlist(
    *, session: AsyncSession, problemstatement_id: UUID, user_id: UUID
):
    try:
        wish = Wishlist(problemstatement_id=problemstatement_id, user_id=user_id)
        session.add(wish)
        await session.commit()
        await session.refresh(wish)
        return wish
    except Exception:
        raise HTTPException(status_code=409, detail="Unable to add.")


async def delete_wishlist(
    *, session: AsyncSession, problemstatement_id: UUID, user_id: UUID
):
    try:
        statement = select(Wishlist).where(
            (Wishlist.problemstatement_id == problemstatement_id)
            & (Wishlist.user_id == user_id)
        )
        problemstatement = (await session.exec(statement=statement)).one_or_none()
        await session.delete(problemstatement)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=409, detail="Unable to delete.")


async def display_wishlist(*, session: AsyncSession, user_id: UUID):
    try:
        statement = (
            select(
                Wishlist.id,
                Problemstatement.id,
                Problemstatement.Name,
                Problemstatement.created_at,
                Problemstatement.problemstatment,
            )
            .join(Wishlist)
            .where(Wishlist.user_id == user_id)
        )
        rows = (await session.exec(statement=statement)).all()
        wishlist = [
            {
                "id": row[0],
                "problemstatement_id": row[1],
                "Name": row[2],
                "created_at": row[3],
                "problemstatement": row[4],
            }
            for row in rows
        ]
        return wishlist
    except Exception:
        raise HTTPException(status_code=404, detail="Not found.")
