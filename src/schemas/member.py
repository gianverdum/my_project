# src/schemas/member.py
from typing import Optional

from pydantic import BaseModel, field_validator


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

    @field_validator("name")
    def name_must_contain_first_and_last(cls, v: str) -> str:
        """Validates that the name contains at least a first name and a last name."""
        if len(v.split()) < 2:
            raise ValueError("Name must contain at least a first name and a last name")
        return v

    @field_validator("phone")
    def phone_must_be_valid(cls, v: str) -> str:
        """Validates that the phone number has exactly 11 digits."""
        if len(v) != 11 or not v.isdigit():
            raise ValueError("Phone number must have exactly 11 digits and contain only numbers")
        return v

    @field_validator("club")
    def club_must_not_be_empty(cls, v: str) -> str:
        """Validates that the club field is not empty."""
        if not v.strip():
            raise ValueError("Club field must not be empty")
        return v


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
