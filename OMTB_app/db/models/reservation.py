import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.user import User
from db.models.showtime import Showtime
from db.models.seat import Seat, SeatSchema
from db import session
from pydantic import BaseModel
from datetime import datetime
from typing import List



Base = declarative_base()

reservation_seat_table = sa.Table(
    'reservation_seat', Base.metadata,
    sa.Column('reservation_id', sa.Integer, sa.ForeignKey('reservations.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('seat_id', sa.Integer, sa.ForeignKey(Seat.id, ondelete='CASCADE'), primary_key=True)
)

class ReservationSchema(BaseModel):
    id: int
    created_at: datetime
    showtime_id: int
    user_id: int
    status: str
    seats: List[SeatSchema] = None
    class Config:
        orm_mode = True

class Reservation(Base):
    __tablename__ = 'reservations'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default='now()')
    showtime_id = sa.Column(sa.Integer, sa.ForeignKey(Showtime.id, ondelete='CASCADE'), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    status = sa.Column(sa.String(255))

    seats = relationship(Seat, secondary=reservation_seat_table)


def check_seats_can_reserved(showtime_id: int, want_seats: list[int]) -> bool:
    reserved_seats = session.query(Reservation).filter_by(showtime_id=showtime_id, status="SUCCESS").all()
    reserved_seats_ids = [seat.id for reservation in reserved_seats for seat in reservation.seats]
    print(f"reserved_seats_ids: {reserved_seats_ids}")
    return all(seat_id not in reserved_seats_ids for seat_id in want_seats)


def create_reservation(showtime_id: int, user_id: int) -> Reservation:
    reservation = Reservation(
        showtime_id=showtime_id,
        user_id=user_id,
        status='PENDING'
    )
    session.add(reservation)
    session.commit()
    return reservation


def get_reserved_seats_by_showtime_id(showtime_id: int) -> List[SeatSchema]:
    reservations = session.query(Reservation).filter_by(showtime_id=showtime_id, status="SUCCESS").all()
    seats = [seat for reservation in reservations for seat in reservation.seats]
    return [SeatSchema.from_orm(seat) for seat in seats]


def get_reservation_by_user_id(user_id: int) -> List[Reservation]:
    reservations = session.query(Reservation).filter_by(user_id=user_id).all()
    return [ReservationSchema.from_orm(reservation) for reservation in reservations]