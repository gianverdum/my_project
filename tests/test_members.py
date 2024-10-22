import pytest
from fastapi.testclient import TestClient
from src.my_project.main import app
from src.my_project.database import MemberDB
from sqlalchemy.orm import Session
from src.my_project.services.members_service import get_db

# Creating a TestClient to simulate requests to the FastAPI app
client = TestClient(app)

# Auto-used pytest fixture to override the get_db dependency
@pytest.fixture(autouse=True)
def override_get_db(db: Session):
    # Overriding the get_db dependency to use the testing session
    app.dependency_overrides[get_db] = lambda: db

    yield db  # Yield the test database session for tests

    # Clean up after the test by removing the override
    app.dependency_overrides.pop(get_db)

# Test case for creating a new member successfully
def test_create_member(override_get_db):
    # Define the new member's details
    new_member = {
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

    # Send a POST request to /members to create the member
    response = client.post("/members", json=new_member)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the returned member's details match the input
    assert response.json() == {
        "id": 1,  # Assuming ID auto-increment starts at 1
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

# Test case for creating a member with missing fields (e.g., missing "club")
def test_create_member_missing_fields(override_get_db):
    incomplete_member = {
        "name": "Jane Doe",
        "phone": "11911112233"
        # Missing "club" field
    }

    # Send a POST request with incomplete data
    response = client.post("/members", json=incomplete_member)

    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert "detail" in response.json()  # Ensure the error message is present

# Test case for creating a member with an invalid phone format
def test_create_member_invalid_phone(override_get_db):
    invalid_phone_member = {
        "name": "Invalid Phone",
        "phone": "invalid_phone",  # Invalid phone number (non-digit characters)
        "club": "Rotary Club of Guarulhos"
    }

    # Send a POST request with invalid phone number
    response = client.post("/members", json=invalid_phone_member)

    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert "detail" in response.json()  # Ensure the error message is present

# Test case for creating a member with empty fields
def test_create_member_empty_fields(override_get_db):
    empty_member = {
        "name": "",
        "phone": "",
        "club": ""
    }

    # Send a POST request with empty fields
    response = client.post("/members", json=empty_member)

    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert "detail" in response.json()  # Ensure the error message is present

# Test case for creating a duplicate member (same phone number)
def test_create_duplicate_member(override_get_db):
    new_member = {
        "name": "Duplicate Member",
        "phone": "11911112244",
        "club": "Rotary Club of Guarulhos"
    }

    # Send the first request to create the member
    response = client.post("/members", json=new_member)
    assert response.status_code == 201  # Ensure the member is created successfully

    # Send the second request with the same data to trigger a duplicate error
    response = client.post("/members", json=new_member)

    # Assert that the response status code is 409 (Conflict)
    assert response.status_code == 409
    assert "detail" in response.json()  # Ensure the error message is present

# Test case for filtering members by name and club
def test_get_all_members_with_filters(override_get_db):
    # Add two members to the database for testing
    client.post("/members", json={"name": "John Doe", "phone": "11911112222", "club": "Rotary Club of Guarulhos"})
    client.post("/members", json={"name": "Jane Smith", "phone": "11911112233", "club": "Rotary Club of São Paulo"})

    # Filter by name
    response = client.get("/members?name=John")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Ensure only one member is returned
    assert response.json()[0]["name"] == "John Doe"  # Verify the member's name

    # Filter by club
    response = client.get("/members?club=São Paulo")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Ensure only one member is returned
    assert response.json()[0]["name"] == "Jane Smith"  # Verify the member's name

    # Filter by both name and club
    response = client.get("/members?name=John&club=Rotary Club of Guarulhos")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Ensure only one member is returned
    assert response.json()[0]["name"] == "John Doe"  # Verify the member's name

# Test case for retrieving members without any filters
def test_get_all_members_without_filters(override_get_db):
    # Send a GET request without filters
    response = client.get("/members")

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "At least one filter ('name' or 'club') must be provided."}  # Validate the error message

# Test case for retrieving members by ID
def test_get_member_by_id(override_get_db):
    # Create a member for testing
    new_member = {"name": "John Doe", "phone": "11911112222", "club": "Rotary Club of Guarulhos"}
    response = client.post("/members", json=new_member)

    # Assuming the first member has ID 1
    response = client.get("/members/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

#Test case for member not found
def test_get_nonexistent_member(override_get_db):
    response = client.get("/members/999") # ID 999 doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Member not found"}
