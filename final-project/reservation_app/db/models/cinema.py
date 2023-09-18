from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cinema(Base):
    __tablename__ = 'cinemas'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default='now()')
    title = Column(String(64), nullable=False)

    # seats = relationship("Seat", backref="cinema")
    # showtimes = relationship("Showtime", backref="cinema")
