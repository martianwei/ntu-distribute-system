import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()


class CinemaSchema(BaseModel):
    id: int
    created_at: datetime
    title: str

    class Config:
        orm_mode = True


class Cinema(Base):
    __tablename__ = 'cinemas'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, server_default=sa.func.now())
    title = sa.Column(sa.String(64), nullable=False)

    # seats = relationship("Seat", backref="cinema")
    # showtimes = relationship("Showtime", backref="cinema")
