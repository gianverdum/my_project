# src/my_project/models/__init__.py

from src.my_project.database.member_db import MemberDB
from src.my_project.models.models import Base, Member

__all__ = ["Base", "Member", "MemberDB"]  # Expose all three models for import
