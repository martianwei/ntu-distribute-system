"""Create SQLAlchemy engine and session objects."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs import configs

# Create database engine
engine = create_engine(configs.POSTGRES_URL)

# Create database session
Session = sessionmaker(bind=engine)
session = Session()
