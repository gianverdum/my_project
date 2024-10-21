import pytest
from fastapi.testclient import TestClient
from src.my_project.main import app

client = TestClient(app)

def test_create_member():
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
        "id": 1, # Assuming the response should return an ID
        "name": "John Doe",
        "phone": "11911112222",
        "club": "Rotary Club of Guarulhos"
    }

# Edge case: Test creating a member with missing fields
def test_create_member_missing_fields():
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
def test_create_member_invalid_phone():
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
def test_create_member_empty_fields():
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
def test_create_duplicate_member():
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
