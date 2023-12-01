from app.utils import get_current_user, get_session
from app.models import User
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


def _validate_user(user: dict):
    if user.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if user.get("description") is None:
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    return user


@router.get("/api/user")
async def get_user():
    user = await get_current_user()
    return JSONResponse(content=user.to_dict(), status_code=200)


@router.get("/api/users")
async def get_users():
    query = select(User)
    session = await get_session()
    users = await session.scalars(query)
    return JSONResponse(content=[user.to_dict() for user in users], status_code=200)


@router.post("/api/user")
async def create_user(user: dict):
    # user = await get_current_user()
    session = await get_session()
    # user = _validate_user(user)

    user = User(
        email=user.get("email"),
        password=user.get("password")
    )
    session.add(user)
    await session.commit()

    return JSONResponse(content=user.to_dict(), status_code=201)
