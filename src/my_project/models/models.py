from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Create a base class for declarative model definitions
Base = declarative_base()


# Define the Member model
class Member(Base):
    __tablename__ = "members"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    phone: str = Column(String(15), unique=True, nullable=False)
    club: str = Column(String(100), nullable=False)


# Ensure Base is available for import
__all__ = ["Base", "Member"]
