# src/services/member_services.py
import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.member import Member
from src.schemas.member import MemberCreate, MemberRead, MemberUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)


def create_member(db: Session, member_data: MemberCreate) -> MemberRead:
    """Inserts a new member into the database."""
    try:
        db_member = Member(**member_data.model_dump())
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return MemberRead.model_validate(db_member)
    except IntegrityError as e:
        if "uq_phone" in str(e.orig):
            raise HTTPException(status_code=400, detail="Phone number already exists")
        raise HTTPException(status_code=500, detail="Database integrity error occurred")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def get_members(db: Session, skip: int = 0, limit: int = 10) -> List[MemberRead]:
    """Retrieves a list of members with pagination."""
    try:
        return db.query(Member).offset(skip).limit(limit).all()
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def get_member_by_id(db: Session, member_id: int) -> Optional[MemberRead]:
    """
    Retrieve a member by their ID.

    Args:
        db (Session): The database session to use for the query.
        member_id (int): The ID of the member to retrieve.

    Returns:
        Optional[MemberRead]: The member record if found; otherwise, raises HTTPException with a 404 status code.

    Raises:
        HTTPException: If the member is not found (404) or if a database error occurs (500).
    """
    try:
        member = db.query(Member).filter(Member.id == member_id).one_or_none()
        if member is None:
            raise HTTPException(status_code=404, detail="Member not found")
        return member
    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")


def update_member(db: Session, member_id: int, updated_data: MemberUpdate) -> Optional[MemberRead]:
    """Updates an existing member's information."""
    try:
        member = get_member_by_id(db, member_id)
        for key, value in updated_data.model_dump().items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
        return member
    except HTTPException:
        # Already handled in get_member_by_id
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def delete_member(db: Session, member_id: int) -> bool:
    """Deletes a member from the database."""
    try:
        member = get_member_by_id(db, member_id)
        db.delete(member)
        db.commit()
        return True
    except HTTPException:
        # Already handled in get_member_by_id
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")
