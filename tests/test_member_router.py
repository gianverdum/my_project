import os  # Ensure this import is included
import random
from typing import Dict, Generator

import pytest
from dotenv import load_dotenv  # Import dotenv to load env variables
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database import Base, get_db
from src.main import app

# Load the database URL from the .env file
load_dotenv()  # Load environment variables from the .env file
DATABASE_URL = os.getenv("POSTGRES_URL")

# Replace the 'postgres://' prefix with 'postgresql://' if necessary
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Remove unwanted string from DATABASE_URL
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("&supa=")[0]

# Raise an error if the DATABASE_URL is missing after loading
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")

# Set up the database engine using the same URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a new DB session for each test."""
    connection = engine.connect()
    transaction = connection.begin()

    # Create a new session for the test
    session = SessionLocal(bind=connection)

    # Optionally, create all tables in the database if they don't exist
    Base.metadata.create_all(bind=engine)

    yield session  # This is where the tests run

    session.close()
    transaction.rollback()  # Roll back the transaction
    connection.close()


@pytest.fixture
def test_client(
    db_session: Session,
) -> Generator[TestClient, None, None]:  # Added type annotation
    """Create a TestClient instance."""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as client:
        yield client


def generate_unique_member() -> Dict[str, str]:
    """Generate a unique member dictionary with random data."""
    return {
        "name": f"Member {random.randint(1, 10000)}",
        "phone": f"119{random.randint(10000000, 99999999)}",
        "club": "Rotary Club of Guarulhos",
    }


def test_add_member(
    test_client: TestClient, db_session: Session
) -> None:  # Added type annotations
    """Test the addition of a new member."""
    # Define the member data to send in the POST request
    member_data = generate_unique_member()

    response = test_client.post("/api/members/", json=member_data)

    assert response.status_code == 200
    response_data = response.json()

    # Check that the response contains the same data we sent, excluding the ID
    assert response_data["club"] == member_data["club"]
    assert response_data["name"] == member_data["name"]
    assert response_data["phone"] == member_data["phone"]

    # Check that an ID is returned and it is a positive integer
    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert response_data["id"] > 0
