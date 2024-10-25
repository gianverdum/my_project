from pydantic import BaseModel


class Member(BaseModel):
    id: int
    name: str
    phone: str
    club: str
