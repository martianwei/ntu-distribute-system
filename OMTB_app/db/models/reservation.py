from sqlalchemy import Column, Integer, DateTime, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.user import User
from db.models.showtime import Showtime
from db.models.seat import Seat
from db import session
import logging

logging.basicConfig(level=logging.INFO)


Base = declarative_base()

reservation_seat_table = Table(
    'reservation_seat', Base.metadata,
    Column('reservation_id', Integer, ForeignKey(
        'reservations.id', ondelete='CASCADE'), primary_key=True),
    Column('seat_id', Integer, ForeignKey(
        Seat.id, ondelete='CASCADE'), primary_key=True)
)


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default='now()')
    showtime_id = Column(Integer, ForeignKey(
        Showtime.id, ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        User.id, ondelete='CASCADE'), nullable=False)
    status = Column(String(255))

    seats = relationship(Seat, secondary=reservation_seat_table)


def check_seats_can_reserved(showtime_id: int, want_seats: list[int]) -> bool:
    logging.info("==========check_seats_can_reserved==========")
    reservations = session.query(Reservation).filter_by(
        showtime_id=showtime_id, status="SUCCESS").all()
    reserved_seats_id = []
    for r in reservations:
        reserved_seats_id.extend([seat.id for seat in r.seats])
    print(f"reserved_seats_id: {reserved_seats_id}")
    check = True
    for seat_id in want_seats:
        if seat_id in reserved_seats_id:
            check = False
            break
    return check
