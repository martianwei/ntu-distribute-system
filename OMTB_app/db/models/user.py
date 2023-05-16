from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default='now()')
    username = Column(String(64), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(64), default=None)
    activated = Column(Boolean, nullable=False)

    reservations = relationship("Reservation", backref="user")
