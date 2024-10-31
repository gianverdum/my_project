# src/schemas/member.py
from typing import Optional

from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str
    phone: str
    club: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "11912345678",
                "club": "Rotary Club of City",
            }
        }


class MemberRead(BaseModel):
    id: int
    name: str
    phone: str
    club: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "11912345678",
                "club": "Rotary Club of City",
            }
        }


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    club: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "11912345678",
                "club": "Rotary Club of City",
            }
        }
