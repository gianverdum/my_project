import pytest
from fastapi.testclient import TestClient
from src.my_project.main import app
from sqlalchemy.orm import Session
from src.my_project.services.members_service import get_db
import random

client = TestClient(app)


@pytest.fixture(scope="function")
def override_get_db(db: Session):
    app.dependency_overrides[get_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_db)


# Helper function to create a unique member
def generate_unique_member():
    return {
        "name": f"Member {random.randint(1, 10000)}",
        "phone": f"119{random.randint(10000000, 99999999)}",
        "club": "Rotary Club of Guarulhos"
    }


# Test case for creating a member with missing fields
def test_create_member_missing_fields(override_get_db):
    incomplete_member = {
        "name": "Jane Doe",
        "phone": "11911112233"
    }
    response = client.post("/members", json=incomplete_member)
    assert response.status_code == 422
    assert "detail" in response.json()


# Test case for creating a member with an invalid phone format
def test_create_member_invalid_phone(override_get_db):
    invalid_phone_member = {
        "name": "Invalid Phone",
        "phone": "invalid_phone",  # Invalid phone number
        "club": "Rotary Club of Guarulhos"
    }
    response = client.post("/members", json=invalid_phone_member)
    assert response.status_code == 422
    assert "detail" in response.json()


# Test case for creating a member with empty fields
def test_create_member_empty_fields(override_get_db):
    empty_member = {
        "name": "",
        "phone": "",
        "club": ""
    }
    response = client.post("/members", json=empty_member)
    assert response.status_code == 422
    assert "detail" in response.json()


# Test case for creating a member and checking for duplicates
def test_create_and_check_duplicate_member(override_get_db):
    new_member = generate_unique_member()

    response = client.post("/members", json=new_member)
    assert response.status_code == 201

    # Attempt to create the same member again
    response = client.post("/members", json=new_member)
    assert response.status_code == 409
    assert "detail" in response.json()


# Test case for creating a member and then retrieving it by ID
def test_create_and_get_member(override_get_db):
    new_member = generate_unique_member()
    response = client.post("/members", json=new_member)
    assert response.status_code == 201
    created_member = response.json()

    response = client.get(f"/members/{created_member['id']}")
    assert response.status_code == 200
    assert response.json() == created_member


# Test case for updating an existing member
def test_update_member(override_get_db):
    new_member = generate_unique_member()
    response = client.post("/members", json=new_member)
    assert response.status_code == 201
    created_member = response.json()

    updated_data = {
        "name": "John Updated",
        "phone": created_member["phone"],  # Same phone used
        "club": "Rotary Club of Guarulhos"
    }
    response = client.put(
        f"/members/{created_member['id']}", json=updated_data)
    assert response.status_code == 200


# Test case for updating a member with invalid phone format
def test_update_member_invalid_phone(override_get_db):
    new_member = generate_unique_member()
    response = client.post("/members", json=new_member)
    assert response.status_code == 201
    created_member = response.json()

    updated_data = {
        "name": "John Updated",
        "phone": "invalid_phone",
        "club": "Rotary Club of Guarulhos"
    }
    response = client.put(
        f"/members/{created_member['id']}", json=updated_data)
    assert response.status_code == 422
    assert "detail" in response.json()


# Test case for updating a non-existent member
def test_update_nonexistent_member(override_get_db):
    updated_data = {
        "name": "Nonexistent Member",
        "phone": "11999999999",
        "club": "Rotary Club of Guarulhos"
    }
    response = client.put("/members/999", json=updated_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Member not found"}


# Test case for filtering members by name
def test_get_all_members_with_filters(override_get_db):
    member1 = generate_unique_member()
    member2 = generate_unique_member()
    client.post("/members", json=member1)
    client.post("/members", json=member2)

    response = client.get(f"/members?name={member1['name']}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == member1["name"]


# Test case for member not found
def test_get_nonexistent_member(override_get_db):
    response = client.get("/members/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Member not found"}


# Test case for deleting an existing member
def test_delete_member_success(override_get_db):
    # Create a new member
    new_member = generate_unique_member()
    response = client.post("/members", json=new_member)
    assert response.status_code == 201
    created_member = response.json()

    # Now attempt to delete the newly created member
    response = client.delete(f"/members/{created_member['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Member deleted successfully"}


# Test case for delete an inexistent member
def test_delete_member_not_found():
    response = client.delete("/members/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Member not found"}
