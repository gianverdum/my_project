from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.my_project.models import Base

# Setup for the test database
SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()  # Provide the session to the test
    # Cleanup after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def override_get_db(db: Session) -> Generator[Session, None, None]:
    yield db
