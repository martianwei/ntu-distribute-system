from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default='now()')
    title = Column(String(64), nullable=False)
    duration = Column(Time, nullable=True)
    category = Column(String(64), nullable=False)

    showtimes = relationship("Showtime", backref="movie")
