from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Database URL for SQLite database file
DATABASE_URL: str = "sqlite:///./members.db"

# Create an engine that connects to the SQLite database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Create a base class for declarative model definitions
Base = declarative_base()


def init_db(connection: Session) -> None:
    # Initialize the database and create all tables defined in the Base.
    Base.metadata.create_all(bind=connection)
