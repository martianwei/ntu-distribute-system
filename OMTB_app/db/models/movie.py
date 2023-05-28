import sqlalchemy as sa
from datetime import time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import session
from pydantic import BaseModel
from typing import Optional, List


Base = declarative_base()


class MovieSchema(BaseModel):
    id: Optional[int]
    title: str
    duration: time
    category: str
    picture_url: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class Movie(Base):
    __tablename__ = 'movies'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, server_default='now()')
    title = sa.Column(sa.String(64), nullable=False)
    duration = sa.Column(sa.Time, nullable=False)
    category = sa.Column(sa.String(64), nullable=False)
    picture_url = sa.Column(sa.String(255), nullable=True)
    description = sa.Column(sa.String(255), nullable=True)
    # showtimes = relationship("Showtime", backref="movie")


def get_all_movies() -> List[MovieSchema]:
    movies = session.query(Movie).all()
    return [MovieSchema.from_orm(movie) for movie in movies]


def get_movie_by_id(movie_id: int) -> Optional[MovieSchema]:
    movie = session.query(Movie).filter_by(id=movie_id).first()
    if movie:
        return MovieSchema.from_orm(movie)
    return None


def insert_movie(movie: MovieSchema) -> MovieSchema:
    movie_data = movie.dict(exclude_unset=True)
    movie_instance = Movie(**movie_data)
    session.add(movie_instance)
    session.commit()
    return MovieSchema.from_orm(movie_instance)
