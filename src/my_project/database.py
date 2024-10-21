from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL for SQLite database file
DATABASE_URL = "sqlite:///./members.db"

# Create an engine that connects to the SQLite database
# `check_same_thread=False` allows the use of the same connection across different threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative model definitions
Base = declarative_base()

def init_db(connection):
    """Initialize the database and create all tables defined in the Base."""
    Base.metadata.create_all(bind=connection)  # Create all tables in the database
