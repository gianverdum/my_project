from pydantic import BaseModel, Field, ValidationError
from pydantic import field_validator

class Member(BaseModel):
    id: int = None
    name: str = Field(..., min_length=1)
    phone: str
    club: str = Field(..., min_length=1)

    @field_validator('phone')
    def validate_phone(cls, v):
        if len(v) != 11 or not v.isdigit():
            raise ValueError('Phone must be exactly 11 digits.')
        return v

    @field_validator('name', 'club')
    def check_empty_fields(cls, v):
        if not v:
            raise ValueError('Field cannot be empty.')
        return v
