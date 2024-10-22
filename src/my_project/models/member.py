from pydantic import BaseModel, Field, ValidationError, ConfigDict
from pydantic import field_validator
from typing import Optional

class Member(BaseModel):
    id: Optional[int] = None  # Use Optional for nullable fields
    name: str = Field(..., min_length=1)
    phone: str
    club: str = Field(..., min_length=1)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('phone')
    def validate_phone(cls, v):
        if len(v) != 11 or not v.isdigit():
            raise ValueError('Phone must be exactly 11 digits.')
        return v

    @field_validator('name', 'club')
    def check_empty_fields(cls, v):
        if not v.strip():  # Ensure no whitespace is considered valid
            raise ValueError('Field cannot be empty.')
        return v

class MemberDB(Member):
    pass  # Add additional fields or methods for the database if needed
