# src/schemas/member.py
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
