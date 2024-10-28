# src/routers/member_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.member import MemberCreate, MemberRead
from src.services.member_services import (
    create_member,
    delete_member,
    get_member_by_id,
    get_members,
    update_member,
)

router = APIRouter()


@router.post("/members/", response_model=MemberRead)
def add_member(member: MemberCreate, db: Session = Depends(get_db)) -> MemberRead:
    return create_member(db, member)


@router.get("/members/", response_model=list[MemberRead])
def list_members(db: Session = Depends(get_db)) -> list[MemberRead]:
    members = get_members(db)
    return [MemberRead.from_orm(member) for member in members]


@router.get("/members/{id}", response_model=MemberRead)
def get_member(id: int, db: Session = Depends(get_db)) -> MemberRead:
    member = get_member_by_id(db, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/members/{id}", response_model=MemberRead)
def modify_member(
    id: int, updated_member: MemberCreate, db: Session = Depends(get_db)
) -> MemberRead:
    member = update_member(db, id, updated_member)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/members/{id}", response_model=dict)
def remove_member(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    success = delete_member(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}
