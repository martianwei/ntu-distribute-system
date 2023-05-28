from typing import Dict, List
from fastapi import APIRouter
from db.models.showtime import get_showtimes_by_movie_id, ShowtimeSchema


router = APIRouter()


@router.get("/showtimes", tags=["showtime"])
async def get_showtimes(movie_id: int) -> Dict[str, List[ShowtimeSchema]]:
    showtimes = get_showtimes_by_movie_id(movie_id)
    return {"showtimes": showtimes}
