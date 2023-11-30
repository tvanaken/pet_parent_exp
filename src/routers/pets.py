from app.models import Breed, Pet
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/pets")
async def get_pets():
    query = select(Pet)
    session = await get_session()
    pets = await session.scalars(query)
    return JSONResponse(content=[pet.to_dict() for pet in pets], status_code=200)