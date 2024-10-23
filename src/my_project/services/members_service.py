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
def get_all_members(db: Session, name: str = None,phone: str = None, club: str = None):
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
    if phone:
        query = query.filter(MemberDB.phone == phone) # Exact match phone

    # Execute the query and return the results
    return query.all()

# Get member by ID
def get_member_by_id(member_id: int, db: Session):
    return db.query(MemberDB).filter(MemberDB.id == member_id).first()

# Update member
def update_member_service(db: Session, member_id: int, member_update: Member):
    """
    Update a member's details in the database.
    :param db: Database session.
    :param member_id: ID of the member to update.
    :param member_update: Member Pydantic model with updated data.
    :return: Updated member object or None if member not found.
    """

    # Fetch the existing member from the database
    existing_member = db.query(MemberDB).filter(MemberDB.id == member_id).first()

    if not existing_member:
        return None #Member not found

    # Update the member's details with the new data
    existing_member.name = member_update.name
    existing_member.phone = member_update.phone
    existing_member.club = member_update.club

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_member) # Refresh to get updated data from the database

    return existing_member
