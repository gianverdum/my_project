from pydantic import BaseModel, Field, ValidationError, ConfigDict
from pydantic import field_validator
from typing import Optional

# Pydantic model for validating the 'Member' data
class Member(BaseModel):
    id: Optional[int] = None  # Optional ID field, typically set after member creation
    name: str = Field(..., min_length=1)  # Name is required and must be at least 1 character long
    phone: str  # Phone number, will be validated
    club: str = Field(..., min_length=1)  # Club is required and must be at least 1 character long

    # Configuration for Pydantic to allow setting fields from ORM models
    model_config = ConfigDict(from_attributes=True)

    # Validator to check if the phone number is exactly 11 digits
    @field_validator('phone')
    def validate_phone(cls, v):
        if len(v) != 11 or not v.isdigit():  # Ensures the phone number is 11 digits and contains only numbers
            raise ValueError('Phone must be exactly 11 digits.')
        return v

    # Validator to ensure name and club fields are not empty or filled with just whitespace
    @field_validator('name', 'club')
    def check_empty_fields(cls, v):
        if not v.strip():  # Trim whitespace and check if the field is empty
            raise ValueError('Field cannot be empty.')
        return v

# MemberDB can inherit from Member for Pydantic validation,
# and additional database-related fields/methods can be added here if necessary.
class MemberDB(Member):
    pass
