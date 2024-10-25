# src/routers/member_router.py
from fastapi import APIRouter

from src.models.member import Member
from src.services.member_services import create_member, get_members

router = APIRouter()


@router.post("/members/", response_model=Member)
def add_member(member: Member) -> Member:
    return create_member(member)


@router.get("/members/", response_model=list[Member])
def list_members() -> list[Member]:
    return get_members()
