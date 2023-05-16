from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Showtime(Base):
    __tablename__ = 'showtimes'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default='now()')
    movie_id = Column(Integer, ForeignKey(
        'movies.id', ondelete='CASCADE'), nullable=False)
    cinema_id = Column(Integer, ForeignKey(
        'cinemas.id', ondelete='CASCADE'), nullable=False)
    movie_start_time = Column(DateTime(timezone=True), nullable=False)

    reservations = relationship("Reservation", backref="showtime")
