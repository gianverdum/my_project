from typing import List, Optional  # Add List import for type hinting

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.my_project.database.member_db import MemberDB  # SQLAlchemy model
from src.my_project.schemas.member import Member  # Pydantic model


# Get members based on filters (name, club, phone)
def get_all_members(
    db: Session,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    club: Optional[str] = None,
) -> List[MemberDB]:  # Return a list of MemberDB
    if not name and not club:
        raise HTTPException(
            status_code=400,
            detail="At least one filter ('name' or 'club') must be provided.",
        )

    # Start the query on the SQLAlchemy model
    query = db.query(MemberDB)

    # Apply the filters dynamically
    if name:
        query = query.filter(MemberDB.name.ilike(f"%{name}%"))
    if club:
        query = query.filter(MemberDB.club.ilike(f"%{club}%"))
    if phone:
        query = query.filter(MemberDB.phone == phone)

    return query.all()


# Update member
def update_member_service(
    db: Session, member_id: int, member_update: Member
) -> Optional[MemberDB]:  # This return type is now Optional[MemberDB]
    existing_member = db.query(MemberDB).filter(MemberDB.id == member_id).first()

    if not existing_member:
        return None

    existing_member.name = member_update.name
    existing_member.phone = member_update.phone
    existing_member.club = member_update.club

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_member)

    return existing_member
