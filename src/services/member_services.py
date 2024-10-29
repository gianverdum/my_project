# src/services/member_services.py
import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.member import Member
from src.schemas.member import MemberCreate, MemberRead, MemberUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)


def create_member(db: Session, member_data: MemberCreate) -> MemberRead:
    try:
        db_member = Member(**member_data.model_dump())
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return MemberRead.model_validate(db_member)
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Database error occurred")


def get_members(db: Session, skip: int = 0, limit: int = 10) -> List[MemberRead]:
    return db.query(Member).offset(skip).limit(limit).all()


def get_member_by_id(db: Session, member_id: int) -> Optional[MemberRead]:
    return db.query(Member).filter(Member.id == member_id).first()


def update_member(
    db: Session, member_id: int, updated_data: MemberUpdate
) -> Optional[MemberRead]:
    member = get_member_by_id(db, member_id)
    if member:
        for key, value in updated_data.model_dump().items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
    return member


def delete_member(db: Session, member_id: int) -> bool:
    member = get_member_by_id(db, member_id)
    if member:
        db.delete(member)
        db.commit()
        return True
    return False
