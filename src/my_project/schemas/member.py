from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Pydantic model for validating the 'Member' data
class Member(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    phone: str
    club: str = Field(..., min_length=1)

    # Configuration for Pydantic to allow setting fields from ORM models
    model_config = ConfigDict(from_attributes=True)

    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if len(v) != 11 or not v.isdigit():
            raise ValueError("Phone must be exactly 11 digits.")
        return v

    @field_validator("name", "club")
    def check_empty_fields(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty.")
        return v


# MemberDB inherit from Member for Pydantic validation
class MemberDB(Member):
    pass
