# src/my_project/models/models.py

import logging  # Import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level
logger = logging.getLogger(__name__)  # Create a logger for this module

logger.info("Loading models.py")  # Log the message


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
