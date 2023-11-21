from app.utils import get_current_user

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


# dummy endpoint (proof of concept)
@router.get("/api/user")
async def get_user():
    user = await get_current_user()
    return JSONResponse(content=user.to_dict(), status_code=200)
