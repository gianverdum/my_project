# src/models/member.py
from sqlalchemy import Column, Integer, String, UniqueConstraint

from src.database import Base


class Member(Base):
    """
    SQLAlchemy model for the members table.

    Attributes:
        id (int): Unique identifier for each member.
        name (str): Name of the member.
        phone (str): Phone number of the member, unique to prevent duplicates.
        club (str): The club associated with the member.

    Constraints:
        uq_phone: Enforces a unique constraint on the phone field.
    """

    __tablename__ = "members"
    __table_args__ = (UniqueConstraint("phone", name="uq_phone"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    club = Column(String, index=True)
