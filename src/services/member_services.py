# src/services/member_services.py
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.member import Member
from src.schemas.member import MemberCreate, MemberRead


def create_member(db: Session, member_data: MemberCreate) -> MemberRead:
    db_member = Member(**member_data.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return MemberRead.from_orm(db_member)


def get_members(db: Session) -> List[Member]:
    return db.query(Member).all()


def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.id == member_id).first()


def update_member(
    db: Session, member_id: int, updated_data: MemberCreate
) -> Optional[Member]:
    member = get_member_by_id(db, member_id)
    if member:
        for key, value in updated_data.dict().items():
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
