from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.cinema import Cinema
from pydantic import BaseModel
from db import session
Base = declarative_base()


class SeatSchema(BaseModel):
    id: int
    cinema_id: int
    seat_number: int

    class Config:
        orm_mode = True


class Seat(Base):
    __tablename__ = 'seats'

    id = sa.Column(sa.Integer, primary_key=True)
    cinema_id = sa.Column(sa.Integer, sa.ForeignKey(
        Cinema.id, ondelete='CASCADE'), nullable=False)
    seat_number = sa.Column(sa.Integer, nullable=False)

    # reservations = relationship("Reservation", backref="seat")
