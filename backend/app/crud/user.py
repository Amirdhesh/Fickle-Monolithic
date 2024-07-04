from app.model import Users, Problemstatement, Solution
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import hash_password, check_pw, create_token
from app.schema.user import userCreate, userUpdate, loginUser, changePassword
from uuid import UUID, uuid4
from app.celery_worker import send_otp_for_forget_password
from app.core.db_init import redis_connection


async def add_user(*, session: AsyncSession, user_create: userCreate):
    try:
        user = Users.model_validate(
            user_create, update={"password": hash_password(user_create.password)}
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=409, detail=f"User already exist.")


async def update_user(*, session: AsyncSession, user_update: userUpdate, id: UUID):
    try:
        user = await session.get(Users, id)
        if not user:
            raise ValueError("User with this id not in the database.")
        user_data = user_update.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_data)
        session.add(user)
        await session.commit()
        await session.refresh()
        return user
    except Exception:
        raise HTTPException(status_code=400, detail=f"User not updated")


async def login_user(*, session: AsyncSession, user_login: loginUser):
    try:
        statement = select(Users).where(Users.email == user_login.email)
        user = (await session.exec(statement=statement)).one_or_none()
        if user:
            if check_pw(user_login.password, user.password):
                return await create_token(id=user.id, email=user.email)
            raise ValueError("Invalid password")
        raise ValueError("Invalid Email/Password")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Unable to login{e}")


async def change_password(*, session: AsyncSession, id: UUID, password: changePassword):
    try:
        user = await session.get(Users, id)
        hashed_password = hash_password(password.new_password)
        user.password = hashed_password
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception:
        raise HTTPException(status_code=400, detail={f"Password not changed."})


async def forget_password_otp(*, session: AsyncSession, email: str):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one_or_none()
        if not user:
            raise ValueError("Invalid Email")
        otp = str(uuid4().int)[-6:]
        send_otp_for_forget_password.delay(email, otp)
        await redis_connection.setex(
            name=f"forget_password_otp:{email}", value=otp, time=600
        )
        return f"OTP has been send to the {email}"
    except Exception:
        raise HTTPException(status_code=400, detail="Unable send OTP.")


async def verifyemail(*, session: AsyncSession, email: str):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one()
        user.email_verified = True
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise Exception(e)


async def profile(*, session: AsyncSession, user_id: UUID):
    try:
        statement = (
            select(Users, Problemstatement, Solution)
            .join(Problemstatement, Users.id == Problemstatement.user_id)
            .join(Solution, Users.id == Solution.user_id)
            .where(Users.id == user_id)
        )
        rows = (await session.exec(statement=statement)).all()
        user_data = None
        problem_statements = []
        solutions = []

        for user, problem, solution in rows:
            if user_data is None:
                user_data = {
                    "id": str(user.id),
                    "email_verified": user.email_verified,
                    "about": user.about,
                    "name": user.Name,
                    "created_at": user.created_at,
                }

            if problem.id not in [ps["id"] for ps in problem_statements]:
                problem_statements.append(
                    {
                        "id": str(problem.id),
                        "Name": problem.Name,
                        "created_at": problem.created_at,
                        "updated_at": problem.updated_at,
                        "problemstatement": problem.problemstatment,
                    }
                )

            if solution.id not in [sol["id"] for sol in solutions]:
                solutions.append(
                    {
                        "id": str(solution.id),
                        "solution_link": solution.solution_link,
                        "solution": solution.solution,
                        "problemstatement_id": solution.problemstatment_id,
                        "created_at": solution.created_at,
                        "updated_at": solution.updated_at,
                    }
                )

        profile_response = {
            "user": user_data,
            "problemstatements": problem_statements,
            "solutions": solutions,
        }
        return profile_response
    except Exception:
        raise HTTPException(status_code=401, detail="Unable to retrive profile.")
