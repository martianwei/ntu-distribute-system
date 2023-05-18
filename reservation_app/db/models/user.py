from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

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

    # reservations = relationship("Reservation", backref="user")


def create_user(session: Session, user: User) -> User:
    """
    Create a new instance of our `User` model.

    :param session: SQLAlchemy database session.
    :type session: Session
    :param user: User data model for creation.
    :type user: User

    :return: User
    """
    try:
        session.add(user)  # Add the user
        session.commit()  # Commit the change
        logging.info(f"Created new user: {user}")
        return user
    except IntegrityError as e:
        logging.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        logging.error(f"Unexpected error when creating user: {e}")
        raise e
