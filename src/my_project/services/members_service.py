from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.my_project.models.member import Member  # Pydantic model
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
    # Check if the member already exists by phone number
    existing_member = db.query(MemberDB).filter(MemberDB.phone == member.phone).first()
    if existing_member:
        raise DuplicateMemberException()  # Raise a custom exception for duplicates

    # Create new member
    new_member = MemberDB(
        name=member.name,
        phone=member.phone,
        club=member.club
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)  # Refresh to get the latest state from the DB
    return new_member

# Get members based on filters (name, club)
def get_all_members(db: Session, name: str = None, club: str = None):
    # Ensure at least one filter is provided
    if not name and not club:
        raise HTTPException(status_code=400, detail="At least one filter ('name' or 'club') must be provided.")

    # Start the query on the SQLAlchemy model
    query = db.query(MemberDB)

    # Apply the filters dynamically
    if name:
        query = query.filter(MemberDB.name.ilike(f"%{name}%"))  # Case-insensitive search for name
    if club:
        query = query.filter(MemberDB.club.ilike(f"%{club}%"))  # Case-insensitive search for club

    # Execute the query and return the results
    return query.all()

# Get member by ID
def get_member_by_id(member_id: int, db: Session):
    return db.query(MemberDB).filter(MemberDB.id == member_id).first()
