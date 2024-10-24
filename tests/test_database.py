import random
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Connection, text

from src.my_project.database import engine, init_db
from src.my_project.main import app

# Create a test client for the FastAPI application
client: TestClient = TestClient(app)


# Setup to run a test with an in-memory database
@pytest.fixture(scope="function")
def test_db() -> Generator[Connection, None, None]:
    connection: Connection = engine.connect()
    transaction = connection.begin()

    init_db(connection)

    yield connection  # Provide the connection to the test functions

    transaction.rollback()
    connection.close()


# Helper function to create a unique member
def generate_unique_member() -> Dict[str, str]:
    return {
        "name": f"Member {random.randint(1, 10000)}",
        "phone": f"119{random.randint(10000000, 99999999)}",
        "club": "Rotary Club of Guarulhos",
    }


# Test to verify the database schema
def test_database_schema(test_db: Connection) -> None:
    result = test_db.execute(text("PRAGMA table_info(members)"))
    columns = result.fetchall()
    expected_columns = ["id", "name", "phone", "club"]

    # Extract the column names from the result
    column_names = [col[1] for col in columns]
    # Assert that the column names match the expected names
    assert column_names == expected_columns


# Test to verify the API connection
def test_api_connection() -> None:
    # Send a GET request to the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Rotary Club API!"}


# Test to verify data insertion into the database
def test_insert_sample_data(test_db: Connection) -> None:
    member = generate_unique_member()  # Generate a unique member

    test_db.execute(
        text(
            "INSERT INTO members(name, phone, club) " "VALUES (:name, :phone, :club);"
        ),
        {"name": member["name"], "phone": member["phone"], "club": member["club"]},
    )

    # Query to retrieve the inserted member
    result = test_db.execute(
        text("SELECT * FROM members WHERE phone = :phone;"), {"phone": member["phone"]}
    )
    inserted_member = result.fetchone()

    assert inserted_member is not None
    assert inserted_member[1] == member["name"]
    assert inserted_member[2] == member["phone"]
    assert inserted_member[3] == member["club"]
