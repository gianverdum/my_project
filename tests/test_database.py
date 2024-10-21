import sqlite3
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from src.my_project.main import app
from src.my_project.database import init_db, engine

# Create a test client for the FastAPI application
client = TestClient(app)

# Setup to run a test with an in-memory database
@pytest.fixture(scope="function")
def test_db():
    # Create a connection to the SQLite in-memory database
    connection = engine.connect()
    transaction = connection.begin()

    # Ensure tables are created in the in-memory database
    init_db(connection)

    yield connection  # Provide the connection to the test functions

    # Revert transaction after the test to rollback any changes
    transaction.rollback()

    # Close the connection at the end of the test
    connection.close()

# Test to verify the database schema
def test_database_schema(test_db):
    # Query to check the columns created in the 'members' table
    result = test_db.execute(text("PRAGMA table_info(members)"))
    columns = result.fetchall()
    expected_columns = ["id", "name", "phone", "club"]

    # Extract the column names from the result
    column_names = [col[1] for col in columns]
    # Assert that the column names match the expected names
    assert column_names == expected_columns

# Test to verify the API connection
def test_api_connection():
    # Send a GET request to the root endpoint
    response = client.get("/")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "Welcome to the Rotary Club API!"}

# Test to verify data insertion into the database
def test_insert_sample_data(test_db):
    # Insert a sample member into the 'members' table
    test_db.execute(text("INSERT INTO members (name, phone, club) VALUES ('Giancarlo Verdum', '11961797970', 'Rotary Club de Guarulhos');"))

    # Query to retrieve the inserted member
    result = test_db.execute(text("SELECT * FROM members WHERE name = 'Giancarlo Verdum';"))
    member = result.fetchone()  # Fetch the first row of the result

    # Verify that the data was inserted correctly
    assert member is not None
    assert member[1] == 'Giancarlo Verdum'
    assert member[2] == '11961797970'
    assert member[3] == 'Rotary Club de Guarulhos'
