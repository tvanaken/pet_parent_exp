from app.models import Task, Breed
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/breeds")
async def get_breeds():
    query = select(Breed)
    session = await get_session()
    breeds = await session.scalars(query)
    return JSONResponse(content=[breed.to_dict() for breed in breeds], status_code=200)