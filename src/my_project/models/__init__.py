# src/my_project/models/__init__.py

import logging  # Import logging

from src.my_project.database.member_db import MemberDB
from src.my_project.models.models import Base, Member

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level
logger = logging.getLogger(__name__)  # Create a logger for this module

logger.info("Loading __init__.py in models")  # Log the message


__all__ = ["Base", "Member", "MemberDB"]  # Expose all three models for import
