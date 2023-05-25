from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from celery import Celery
from pydantic import BaseModel
from exception import LockAcquisitionError, SeatHasReservedError
from configs import configs
from db import session
from db.models.reservation import Reservation, check_seats_can_reserved
from db.models.seat import Seat
from db.models.movie import Movie
from db.models.showtime import Showtime
from lock.redis import get_lock, release_locks
import logging

logging.basicConfig(level=logging.INFO)
celery_app = Celery(configs.APP_NAME)
celery_app.conf.update(
    broker_url=configs.CELERY_BROKER_URL,  # broker，注意rabbitMQ的VHOST要给你使用的用户加权限
    result_backend=configs.CELERY_RESULT_BACKEND,  # backend配置，注意指定redis数据库
)


router = APIRouter()


class reservationRequest(BaseModel):
    user_id: str
    showtime_id: str
    cinema_id: int
    seat_numbers: list[int]


@router.post("/main_page/reserve", tags=["main_page"])
async def reserve(request: reservationRequest):
    seats = session.query(Seat).filter(
        Seat.cinema_id == request.cinema_id, Seat.seat_number.in_(request.seat_numbers)).all()
    seat_ids = [seat.id for seat in seats]
    logging.info(f"seat_ids: {seat_ids}")
    locks = []
    try:
        can_reserve = check_seats_can_reserved(
            request.showtime_id, seat_ids)
        if not can_reserve:
            raise SeatHasReservedError(
                f"Seat has been reserved for showtime ID: {request.showtime_id}")
        # Acquire locks for each seat ID
        for seat_id in seat_ids:
            lock_key = f"showtime_id={request.showtime_id} seat_num={seat_id}"
            lock = get_lock(lock_key)
            if lock is None:
                raise LockAcquisitionError(
                    f"Failed to acquire lock for showtime ID: {request.showtime_id} seat ID: {seat_id}")
            locks.append(lock)

    except LockAcquisitionError:
        # Release all acquired locks if any lock acquisition fails
        release_locks(locks)
        return JSONResponse(
            content={"msg": "the seat have been lock!!!"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
    except SeatHasReservedError:
        return JSONResponse(
            content={"msg": "the seat have been reserved!!!"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
    # Create a new reservation instance
    reservation = Reservation(
        showtime_id=request.showtime_id,
        user_id=request.user_id,
        status='PENDING'
    )

    # Add the reservation to the session
    session.add(reservation)

    # Commit the session to persist the changes to the database
    session.commit()

    task = celery_app.send_task(
        "reservation_app.tasks.reservation",
        queue="movie_reservation_queue",
        args=[reservation.id, seat_ids],
    )

    return JSONResponse(
        content={"msg": "reserve request success", "taskid": str(task.id)},
        status_code=HTTPStatus.OK,
    )


@router.get("/main_page/movies", tags=["main_page"])
async def get_movies(movie_id: int = None) -> dict:
    if movie_id is None:
        movies = session.query(Movie).all()
        return {
            "movies": [
                {
                    "movie_id": movie.id,
                    "title": movie.title,
                    # "pic_url": movie.pic_url,
                } for movie in movies
            ]
        }
    else:
        movies = session.query(Movie).filter_by(id=movie_id).all()
        if len(movies) == 0:
            return {"Error": "No such movie"}
        
        movie = movies[0]
        return {
            "title": movie.title,
            # "description": movie.description,
            "duration": movie.duration,
            "category": movie.category,
            # "pic_url": movie.pic_url,
        }


@router.get("/main_page/showtimes", tags=["main_page"])
async def get_showtimes(movie_id: int) -> dict:
    showtimes = session.query(Showtime).filter_by(movie_id=movie_id).all()
    return {
        "showtimes": [
            {
                "showtime_id": showtime.id,
                "movie_starttime": showtime.movie_start_time,
            }  for showtime in showtimes
        ]
    }

# TODO
@router.get("/main_page/reserved_seats", tags=["main_page"])
async def get_showtimes(showtime_id: int) -> dict:
    return {
        "cinema_id": 1,
        "reserved_seat_numbers": [1, 2, 3]
    }
