# src/services/member_services.py
from src.models.member import Member

member_db = []


def create_member(member: Member) -> Member:
    member_db.append(member)
    return member


def get_members() -> list[Member]:
    return member_db
