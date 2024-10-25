# src/my_project/schemas/member.py

from typing import Optional, Type
from pydantic import BaseModel, ConfigDict, Field, field_validator


class MemberSchema(BaseModel):  # Renamed to avoid confusion
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    phone: str
    club: str = Field(..., min_length=1)

    model_config: Type[ConfigDict] = ConfigDict(from_attributes=True)

    @field_validator("phone")
    def validate_phone(cls: Type[BaseModel], v: str) -> str:
        if len(v) != 11 or not v.isdigit():
            raise ValueError("Phone must be exactly 11 digits.")
        return v

    @field_validator("name", "club")
    def check_empty_fields(cls: Type[BaseModel], v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty.")
        return v
