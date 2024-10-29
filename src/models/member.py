# src/models/member.py
from sqlalchemy import Column, Integer, String, UniqueConstraint

from src.database import Base


class Member(Base):
    __tablename__ = "members"
    __table_args__ = (UniqueConstraint("phone", name="uq_phone"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    club = Column(String, index=True)
