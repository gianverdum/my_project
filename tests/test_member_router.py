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
    if transaction.is_active:
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


def test_member_creation_success(test_client: TestClient, db_session: Session) -> None:
    """Validates that a new member can be added successfully via POST request.

    This test sends member data, checks that the response status is 200,
    verifies the returned data matches the input (excluding ID),
    and confirms the presence and type of the member ID.
    """
    # Arrange
    member_data = generate_unique_member()

    # Act
    response = test_client.post("/api/members/", json=member_data)

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["club"] == member_data["club"]
    assert response_data["name"] == member_data["name"]
    assert response_data["phone"] == member_data["phone"]
    assert "id" in response_data and isinstance(response_data["id"], int) and response_data["id"] > 0


def test_member_creation_duplicate_phone_number(test_client: TestClient, db_session: Session) -> None:
    """Validates that isn't possible to add a new member with a duplicate
    phone number via POST request.
    """
    # Arrange
    member_data = generate_unique_member()
    duplicate_number = {
        "name": "Duplicate phone",
        "phone": member_data["phone"],
        "club": "Rotary Club of Guarulhos",
    }

    # Act
    response1 = test_client.post("/api/members", json=member_data)
    response2 = test_client.post("/api/members", json=duplicate_number)

    # Assert
    assert response1.status_code == 201

    assert response2.status_code == 400
    # Allow flexibility in key name by checking both possibilities
    error_message = response2.json().get("detail") or response2.json().get("message")
    assert error_message == "Phone number already exists"


def test_member_creation_missing_required_fields(test_client: TestClient, db_session: Session) -> None:
    """Validates that it's not possible to add a new member with a missing required field via POST request."""

    # Arrange
    missing_name = {
        "phone": "11912345678",
        "club": "Rotary Club of Guarulhos",
    }
    missing_phone = {
        "name": "John Doe",
        "club": "Rotary Club of Guarulhos",
    }
    missing_club = {
        "name": "John Doe",
        "phone": "11912345678",
    }

    # Act & Assert
    response1 = test_client.post("/api/members", json=missing_name)
    assert response1.status_code == 422
    assert response1.json()["detail"][0]["msg"] == "Field required"
    assert response1.json()["detail"][0]["loc"] == ["body", "name"]

    response2 = test_client.post("/api/members", json=missing_phone)
    assert response2.status_code == 422
    assert response2.json()["detail"][0]["msg"] == "Field required"
    assert response2.json()["detail"][0]["loc"] == ["body", "phone"]

    response3 = test_client.post("/api/members", json=missing_club)
    assert response3.status_code == 422
    assert response3.json()["detail"][0]["msg"] == "Field required"
    assert response3.json()["detail"][0]["loc"] == ["body", "club"]


def test_member_creation_invalid_name_format(test_client: TestClient, db_session: Session) -> None:
    """Validates that it's not possible to add a new member with an invalid name format via POST request."""

    invalid_name_data = {
        "name": "John",  # Invalid: should contain both first and last names
        "phone": "11912345678",
        "club": "Rotary Club of Guarulhos",
    }

    response = test_client.post("/api/members", json=invalid_name_data)
    assert response.status_code == 422
    details = response.json().get("detail")
    assert any(
        "name" in error["loc"] and "Name must contain at least a first name and a last name" in error["msg"]
        for error in details
    )


def test_member_creation_invalid_phone_format(test_client: TestClient, db_session: Session) -> None:
    """Validates that it's not possible to add a new member with an invalid phone format via POST request."""

    invalid_phone_data = {
        "name": "John Doe",
        "phone": "123",  # Invalid: should have 11 digits
        "club": "Rotary Club of Guarulhos",
    }

    response = test_client.post("/api/members", json=invalid_phone_data)
    assert response.status_code == 422
    details = response.json().get("detail")
    assert any(
        "phone" in error["loc"] and "Phone number must have exactly 11 digits and contain only numbers" in error["msg"]
        for error in details
    )


def test_member_creation_empty_club(test_client: TestClient, db_session: Session) -> None:
    """Validates that it's not possible to add a new member with an empty club field via POST request."""

    empty_club_data = {
        "name": "John Doe",
        "phone": "11912345678",
        "club": "",  # Invalid: should not be empty
    }

    response = test_client.post("/api/members", json=empty_club_data)
    assert response.status_code == 422
    details = response.json().get("detail")
    assert any("club" in error["loc"] and "Club field must not be empty" in error["msg"] for error in details)


def test_get_members_success(test_client: TestClient, db_session: Session) -> None:
    """Validates that the API can retrieve a list of members successfully."""
    # Arrange
    member_data1 = generate_unique_member()
    member_data2 = generate_unique_member()

    test_client.post("/api/members/", json=member_data1)
    test_client.post("/api/members/", json=member_data2)

    # Act
    response = test_client.get("/api/members/")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) >= 2  # Ensure at least 2 members are returned


def test_get_member_by_id_success(test_client: TestClient, db_session: Session) -> None:
    """Validates that a specific member can be retrieved by ID."""
    # Arrange
    member_data = generate_unique_member()
    response = test_client.post("/api/members/", json=member_data)
    member_id = response.json()["id"]

    # Act
    response = test_client.get(f"/api/members/{member_id}")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == member_id
    assert response_data["name"] == member_data["name"]
    assert response_data["phone"] == member_data["phone"]
    assert response_data["club"] == member_data["club"]


def test_get_member_by_id_not_found(test_client: TestClient, db_session: Session) -> None:
    """Validates that trying to retrieve a non-existing member by ID returns a 404 error."""
    # Act
    response = test_client.get("/api/members/999")  # Assuming 999 does not exist

    # Assert
    print(response.content)
    assert response.status_code == 404

    # Allow flexibility in key name by checking both possibilities
    error_message = response.json().get("detail") or response.json().get("message")
    assert error_message == "Member not found"  # This line remains unchanged


def test_update_member_success(test_client: TestClient, db_session: Session) -> None:
    """Validates that a member's data can be updated successfully."""
    # Arrange
    member_data = generate_unique_member()
    response = test_client.post("/api/members/", json=member_data)
    member_id = response.json()["id"]

    updated_data = {"name": "Updated Name", "phone": "11987654321", "club": "Updated Club"}

    # Act
    response = test_client.put(f"/api/members/{member_id}", json=updated_data)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == member_id
    assert response_data["name"] == updated_data["name"]
    assert response_data["phone"] == updated_data["phone"]
    assert response_data["club"] == updated_data["club"]


def test_update_member_not_found(test_client: TestClient, db_session: Session) -> None:
    """Validates that trying to update a non-existing member returns a 404 error."""
    # Act
    response = test_client.put("/api/members/999", json={"name": "Some Name"})

    # Assert
    print(response.content)
    assert response.status_code == 404

    # Allow flexibility in key name by checking both possibilities
    error_message = response.json().get("detail") or response.json().get("message")
    assert error_message == "Member not found"


def test_delete_member_success(test_client: TestClient, db_session: Session) -> None:
    """Validates that a member can be deleted successfully."""
    # Arrange
    member_data = generate_unique_member()
    response = test_client.post("/api/members/", json=member_data)
    member_id = response.json()["id"]

    # Act
    response = test_client.delete(f"/api/members/{member_id}")

    # Assert
    print(response.content)
    assert response.status_code == 204

    # Confirm that the member no longer exists
    response = test_client.get(f"/api/members/{member_id}")
    print(response.content)
    assert response.status_code == 404


def test_delete_member_not_found(test_client: TestClient, db_session: Session) -> None:
    """Validates that trying to delete a non-existing member returns a 404 error."""
    # Act
    response = test_client.delete("/api/members/999")  # Assuming 999 does not exist

    # Assert
    print(response.content)
    assert response.status_code == 404

    # Allow flexibility in key name by checking both possibilities
    error_message = response.json().get("detail") or response.json().get("message")
    assert error_message == "Member not found"
