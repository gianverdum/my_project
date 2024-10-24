from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Create a base class for declarative model definitions
Base = declarative_base()


# Define the Member model
class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    club = Column(String(100), nullable=False)


# Ensure Base is available for import
__all__ = ["Base", "Member"]
