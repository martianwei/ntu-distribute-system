import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.models.movie import Movie, MovieSchema
from db.models.cinema import Cinema
from pydantic import BaseModel
from datetime import datetime
from db import session
Base = declarative_base()


class ShowtimeSchema(BaseModel):
    id: int
    created_at: datetime
    # movie_id: int
    cinema_id: int
    movie_start_time: datetime
    movie: MovieSchema = None

    class Config:
        orm_mode = True


class Showtime(Base):
    __tablename__ = 'showtimes'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, server_default='now()')
    movie_id = sa.Column(sa.Integer, sa.ForeignKey(
        Movie.id, ondelete='CASCADE'), nullable=False)
    cinema_id = sa.Column(sa.Integer, sa.ForeignKey(
        Cinema.id, ondelete='CASCADE'), nullable=False)
    movie_start_time = sa.Column(sa.DateTime(timezone=True), nullable=False)
    movie = relationship(Movie, backref='showtimes')


def get_showtimes_by_movie_id(movie_id: int) -> ShowtimeSchema:
    showtimes = session.query(Showtime).filter_by(movie_id=movie_id).all()
    return [ShowtimeSchema.from_orm(showtime) for showtime in showtimes]
