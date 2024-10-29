# src/routers/member_router.py
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.member import MemberCreate, MemberRead, MemberUpdate
from src.services.member_services import (
    create_member,
    delete_member,
    get_member_by_id,
    get_members,
    update_member,
)

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.post("/members/", response_model=MemberRead)
def add_member(member: MemberCreate, db: Session = Depends(get_db)) -> MemberRead:
    return create_member(db, member)


@router.get("/members/", response_model=list[MemberRead])
def list_members(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[MemberRead]:
    members = get_members(db, skip=skip, limit=limit)
    return [MemberRead.model_validate(member) for member in members]


@router.get("/members/{id}", response_model=MemberRead)
def get_member(id: int, db: Session = Depends(get_db)) -> MemberRead:
    member = get_member_by_id(db, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/members/{id}", response_model=MemberRead)
def modify_member(
    id: int, updated_member: MemberUpdate, db: Session = Depends(get_db)
) -> MemberRead:
    member = update_member(db, id, updated_member)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/members/{id}", status_code=204)
def remove_member(id: int, db: Session = Depends(get_db)) -> None:
    success = delete_member(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
