from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.my_project.schemas.member import Member  # Pydantic model
from src.my_project.database.member_db import MemberDB  # SQLAlchemy model
from src.my_project.database import SessionLocal


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Custom exception for duplicate members
class DuplicateMemberException(Exception):
    pass


# Create a new member
def create_member(member: Member, db: Session):
    existing_member = db.query(MemberDB).filter(
        MemberDB.phone == member.phone).first()
    if existing_member:
        raise DuplicateMemberException()

    # Create new member
    new_member = MemberDB(
        name=member.name,
        phone=member.phone,
        club=member.club
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


# Get members based on filters (name, club)
def get_all_members(
    db: Session,
    name: str = None,
    phone: str = None,
    club: str = None
):
    if not name and not club:
        raise HTTPException(
            status_code=400,
            detail="At least one filter ('name' or 'club') must be provided.")

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


# Get member by ID
def get_member_by_id(member_id: int, db: Session):
    return db.query(MemberDB).filter(MemberDB.id == member_id).first()


# Update member
def update_member_service(db: Session, member_id: int, member_update: Member):
    existing_member = db.query(MemberDB).filter(
        MemberDB.id == member_id).first()

    if not existing_member:
        return None

    existing_member.name = member_update.name
    existing_member.phone = member_update.phone
    existing_member.club = member_update.club

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_member)

    return existing_member


# Delete member
def delete_member(member_id: int, db: Session):
    member = db.query(MemberDB).filter(
        MemberDB.id == member_id).first()
    if member:
        db.delete(member)
        db.commit()
        return True
    return False
