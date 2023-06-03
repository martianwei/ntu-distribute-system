from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import session

Base = declarative_base()


class UserSchema(BaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    username: str
    email: str
    password: str
    activated: bool

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, server_default='now()')
    username = sa.Column(sa.String(64), nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(64), default=None)
    activated = sa.Column(sa.Boolean, nullable=False)

    # reservations = relationship("Reservation", backref="user")


def create_user(user: UserSchema) -> UserSchema:
    try:
        user_data = user.dict(exclude_unset=True)
        user_instance = User(**user_data)
        session.add(user_instance)
        session.commit()
        return UserSchema.from_orm(user_instance)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")


def get_user_by_username(username: str) -> Optional[UserSchema]:
    user = session.query(User).filter(User.username == username).first()
    if user:
        return UserSchema.from_orm(user)
    print(f"User {username} not found")
    return None
