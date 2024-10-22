import pytest
from fastapi.testclient import TestClient
from src.my_project.main import app
from src.my_project.database import MemberDB
from sqlalchemy.orm import Session
from src.my_project.services.members_service import get_db

client = TestClient(app)

# This test must run with the database fixture
@pytest.fixture(autouse=True)
def override_get_db(db: Session):
    # Overriding the get_db dependency to use the testing session
    app.dependency_overrides[get_db] = lambda: db

    yield db  # Return the test database session

    # Clean up after the test
    app.dependency_overrides.pop(get_db)

def test_create_member(override_get_db):
    new_member = {
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

    # Send a POST request to /members
    response = client.post("/members", json=new_member)

    # Check if the response status code is 201 Created
    assert response.status_code == 201

    # Check if the response contains the created member's details
    assert response.json() == {
        "id": 1,  # Assuming the response should return an ID
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

# Edge case: Test creating a member with missing fields
def test_create_member_missing_fields(override_get_db):
    incomplete_member = {
        "name": "Jane Doe",
        "phone": "11911112233"
        # Missing "club"
    }

    response = client.post("/members", json=incomplete_member)

    # Check if the response status code is 422 Unprocessable Entity
    assert response.status_code == 422
    assert "detail" in response.json()

# Edge case: Test creating a member with invalid phone format
def test_create_member_invalid_phone(override_get_db):
    invalid_phone_member = {
        "name": "Invalid Phone",
        "phone": "invalid_phone",
        "club": "Rotary Club of Guarulhos"
    }

    response = client.post("/members", json=invalid_phone_member)

    # Check if the response status code is 422 Unprocessable Entity
    assert response.status_code == 422
    assert "detail" in response.json()

# Edge case: Test creating a member with empty fields
def test_create_member_empty_fields(override_get_db):
    empty_member = {
        "name": "",
        "phone": "",
        "club": ""
    }

    response = client.post("/members", json=empty_member)

    # Check if the response status code is 422 Unprocessable Entity
    assert response.status_code == 422
    assert "detail" in response.json()

# Edge case: Test creating a duplicate member
def test_create_duplicate_member(override_get_db):
    new_member = {
        "name": "Duplicate Member",
        "phone": "11911112244",
        "club": "Rotary Club of Guarulhos"
    }

    # First request to create the member
    response = client.post("/members", json=new_member)
    assert response.status_code == 201

    # Second request to create the same member
    response = client.post("/members", json=new_member)

    # Check if the response status code is 409 Conflict
    assert response.status_code == 409
    assert "detail" in response.json()

def test_get_all_members_with_filters(override_get_db):
    client.post("/members", json={"name": "John Doe", "phone": "11911112222", "club": "Rotary Club of Guarulhos"})
    client.post("/members", json={"name": "Jane Smith", "phone": "11911112233", "club": "Rotary Club of São Paulo"})

    response = client.get("/members?name=John")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "John Doe"

    response = client.get("/members?club=São Paulo")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Jane Smith"

    response = client.get("/members?name=John&club=Rotary Club of Guarulhos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "John Doe"

def test_get_all_members_without_filters(override_get_db):
    response = client.get("/members")
    # Check if the response status code is 400
    assert response.status_code == 400
    assert response.json() == {"detail": "At least one filter ('name' or 'club') must be provided."}
