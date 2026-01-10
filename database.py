import os
import time
from sqlalchemy.exc import OperationalError
from sqlmodel import create_engine, SQLModel, Session

# Priority: Environment variable from Docker Compose, then .env file
DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg2://train:Ankara06@localhost:5432/traindb",
)

# Use pool_pre_ping to handle connection drops
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)


def create_db_and_tables():
    """Retries connection to DB until it's ready, then creates tables."""
    retries = 5
    while retries > 0:
        try:
            SQLModel.metadata.create_all(engine)
            print("Successfully connected to Database and created tables.")
            break
        except OperationalError:
            print(
                f"Database not ready yet... Retrying in 5 seconds. ({retries} retries left)"
            )
            retries -= 1
            time.sleep(5)


def get_db():
    """Provides a transactional session for API requests."""
    with Session(engine) as session:
        yield session
