from datetime import datetime
from app.models import Reminder
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


async def _validate_reminder(reminder: dict):
    if reminder.get("type") is None:
        raise HTTPException(status_code=400, detail="Must define a type")
    if reminder.get("frequency") is None:
        raise HTTPException(status_code=400, detail="Must state a frequency")
    if reminder.get("start_date") is None:
        raise HTTPException(status_code=400, detail="Must give a start date")
    return reminder


async def _get_reminder(reminder_id: int):
    session = await get_session()
    user = await get_current_user()
    query = select(Reminder).where(Reminder.id == reminder_id).where(Reminder.user_id == user.id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/reminders")
async def get_reminders():
    query = select(Reminder)
    session = await get_session()
    reminders = await session.scalars(query)
    return JSONResponse(content=[reminder.to_dict() for reminder in reminders], status_code=200)


@router.get("/api/reminders/{user_id}")
async def get_user_reminders(user_id: int):
    session = await get_session()
    user = await get_current_user()
    if user.id == user_id or user.id == 1:
        query = select(Reminder).where(Reminder.user_id == user_id)
        reminders = await session.scalars(query)
        return JSONResponse(content=[reminder.to_dict() for reminder in reminders], status_code=200)
    else:
        return JSONResponse(content={"message": "Not authorized"}, status_code=404)
    

@router.post("/api/reminders")
async def create_reminder(reminder: dict):
    user = await get_current_user()
    session = await get_session()
    reminder = await _validate_reminder(reminder)

    # if reminder:
    start_date_str = reminder.get("start_date")
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    else:
        start_date = None

    end_date_str = reminder.get("end_date")
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = None

    reminder = Reminder(
        user_id = user.id,
        type=reminder.get("type"),
        frequency=reminder.get("frequency"),
        start_date=start_date,
        end_date=end_date
    )
    session.add(reminder)
    await session.commit()

    return JSONResponse(content=reminder.to_dict(), status_code=201)


@router.delete("/api/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int):
    user = await get_current_user()
    session = await get_session()
    reminder = await _get_reminder(reminder_id)
    if reminder:
        await session.delete(reminder)
        await session.commit()
        return JSONResponse(content={"message": "Reminder deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Reminder not found"}, status_code=404)


@router.patch("/api/reminders/{reminder_id}")
async def update_reminder(reminder_id: int, reminder_updates: dict):
    session = await get_session()
    reminder = await _get_reminder(reminder_id)

    if not reminder:
        return JSONResponse(content={"message": "Reminder not found"}, status_code=404)
    
    if reminder_updates.get("type") is not None:
        reminder.type = reminder_updates.get("type")
    if reminder_updates.get("frequency") is not None:
        reminder.frequency = reminder_updates.get("frequency")
    if reminder_updates.get("start_date") is not None:
        start_date_str = reminder_updates.get("start_date")
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        else:
            start_date = None
        reminder.start_date = start_date
    if reminder_updates.get("end_date") is not None:
        end_date_str = reminder_updates.get("end_date")
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        else:
            end_date = None
        reminder.end_date = end_date

    await session.commit()

    return JSONResponse(content=reminder.to_dict(), status_code=200)