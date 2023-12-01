from app.models import Breed, Pet
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


def _validate_pet(pet: dict):
    if pet.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if pet.get("breed") is None:
        raise HTTPException(status_code=400, detail="Breed cannot be empty")
    return pet


async def _get_pet(pet_id: int):
    session = await get_session()
    user = await get_current_user()
    query = select(Pet).where(Pet.id == pet_id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/pets")
async def get_pets():
    query = select(Pet)
    session = await get_session()
    pets = await session.scalars(query)
    return JSONResponse(content=[pet.to_dict() for pet in pets], status_code=200)


@router.get("/api/pets/{pet_id}")
async def get_pet(pet_id: int):
    breed = await _get_pet(pet_id)
    if breed:
        return breed.to_dict()
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)
    

@router.post("/api/pets")
async def create_pet(pet: dict):
    session = await get_session()
    breed = _validate_breed(breed)

    breed = Breed(
        name=breed.get("name"),
        suggested_supplements=breed.get("suggested_supplements"),
        suggested_exercise=breed.get("suggested_exercise"),
    )
    session.add(breed)
    await session.commit()

    return JSONResponse(content=breed.to_dict(), status_code=201)