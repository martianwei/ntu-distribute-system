from sqlalchemy import Column, Integer, DateTime, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.user import User
from db.models.showtime import Showtime
from db.models.seat import Seat

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
