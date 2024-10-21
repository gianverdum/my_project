from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Create a base class for declarative model definitions
Base = declarative_base()

# Define the Member model
class Member(Base):
    __tablename__ = 'members'  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for each member
    name = Column(String(100), nullable=False)  # Member's name, cannot be null
    phone = Column(String(15), unique=True, nullable=False)  # Member's phone number, must be unique and cannot be null
    club = Column(String(100), nullable=False)  # Name of the club to which the member belongs, cannot be null
