# src/test_connection.py
from sqlalchemy import create_engine

# Hardcoded database connection details
USERNAME = "postgres"  # Your database username
PASSWORD = "09tywYLvBRcgmkG6"  # Your database password
HOST = "aws-0-us-east-1.pooler.supabase.com"  # Your database host
PORT = "6543"  # Your database port
DATABASE_NAME = "postgres"  # Your database name
SSL_MODE = "require"  # SSL mode setting

# Construct the database URL
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}?sslmode={SSL_MODE}"

print(f"DATABASE_URL: {DATABASE_URL}")  # Debugging print statement

try:
    # Create a database engine
    engine = create_engine(DATABASE_URL)
    # Connect to the database
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
