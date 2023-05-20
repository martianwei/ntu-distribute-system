from db import session
from db.models.reservation import Reservation
from db.models.seat import Seat
from . import celery_app
from utils.check_param import check_parameter
import logging


@celery_app.task(
    name="reservation_app.tasks.reservation",
)  # 常駐等待
def reservation(*args):
    # check_parameter(args, "args", tuple)
    # check_parameter(args[0], "reservation_id", int)
    # check_parameter(args[1], "seat_ids", list[int])
    reservation_id = args[0]
    seat_ids = args[1]
    logging.info(f"1111 reservation_id: {reservation_id}")
    logging.info(f"1111 seat_ids: {seat_ids}")
    try:
        # Retrieve the reservation instance
        reservation = session.query(Reservation).filter_by(
            id=reservation_id).first()
        logging.info(f"reservation: {reservation}")
        # Create seat instances and associate them with the reservation
        seats = []
        for seat_id in seat_ids:
            seat = session.query(Seat).filter_by(id=seat_id).first()
            seats.append(seat)
        logging.info(f"seats: {seats}")
        reservation.seats = seats

        # Update the reservation status
        reservation.status = "SUCCESS"

        session.commit()

    except Exception as e:
        # Retrieve the reservation instance
        reservation = session.query(Reservation).filter_by(
            id=reservation_id).first()

        # Update the reservation status
        reservation.status = "FAILED"

        logging.error(e)
        raise
