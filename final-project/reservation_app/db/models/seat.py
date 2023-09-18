from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.cinema import Cinema

Base = declarative_base()


class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey(
        Cinema.id, ondelete='CASCADE'), nullable=False)
    seat_number = Column(Integer, nullable=False)

    # reservations = relationship("Reservation", backref="seat")
