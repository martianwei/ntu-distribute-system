from typing import Dict, List
from fastapi import APIRouter
from db.models.reservation import get_reserved_seats_by_showtime_id

router = APIRouter()


@router.get("/seats", tags=["seat"])
async def get_reserved_seats(showtime_id: int) -> dict:
    seats = get_reserved_seats_by_showtime_id(showtime_id)
    return {"seats": seats}
