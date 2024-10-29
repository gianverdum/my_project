# src/schemas/member.py
from typing import Optional

from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str
    phone: str
    club: str


class MemberRead(BaseModel):
    id: int
    name: str
    phone: str
    club: str

    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    club: Optional[str] = None
