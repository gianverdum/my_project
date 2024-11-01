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
    """
    Inserts a new member into the database.

    Args:
        db (Session): The active SQLAlchemy session.
        member_data (MemberCreate): Data required to create the member.

    Returns:
        MemberRead: The created member object.

    Raises:
        HTTPException: If there is a database error or any unexpected issue.
    """
    try:
        db_member = Member(**member_data.model_dump())
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return MemberRead.model_validate(db_member)
    except IntegrityError as e:
        if "uq_phone" in str(e.orig):
            raise HTTPException(status_code=400, detail="Phone number already exists")
        raise HTTPException(status_code=500, detail="Database integrity error ocurred")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def get_members(db: Session, skip: int = 0, limit: int = 10) -> List[MemberRead]:
    """
    Retrieves a list of members with pagination.

    Args:
        db (Session): Database session used to perform operations.
        skip (int): The number of records to skip, used for pagination.
        limit (int): The maximum number of records to retrieve.

    Returns:
        List[MemberRead]: List of member records.

    Raises:
        HTTPException: If an unexpected error occurs.
    """
    try:
        return db.query(Member).offset(skip).limit(limit).all()
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def get_member_by_id(db: Session, member_id: int) -> Optional[MemberRead]:
    """
    Retrieves a member by their ID.

    Args:
        db (Session): Database session used to perform operations.
        member_id (int): The unique identifier of the member.

    Returns:
        Optional[MemberRead]: The member data if found, otherwise None.

    Raises:
        HTTPException: If an unexpected error occurs.
    """
    try:
        return db.query(Member).filter(Member.id == member_id).first()
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def update_member(
    db: Session, member_id: int, updated_data: MemberUpdate
) -> Optional[MemberRead]:
    """
    Updates an existing member's information.

    Args:
        db (Session): Database session used to perform operations.
        member_id (int): The unique identifier of the member.
        updated_data (MemberUpdate): The data to update the member with.

    Returns:
        Optional[MemberRead]: The updated member's data if found, \
            otherwise None.

    Raises:
        HTTPException: If a database or other unexpected error occurs.
    """
    try:
        member = get_member_by_id(db, member_id)
        if member:
            for key, value in updated_data.model_dump().items():
                setattr(member, key, value)
            db.commit()
            db.refresh(member)
        return member
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


def delete_member(db: Session, member_id: int) -> bool:
    """
    Deletes a member from the database.

    Args:
        db (Session): Database session used to perform operations.
        member_id (int): The unique identifier of the member.

    Returns:
        bool: True if the member was deleted, otherwise False.

    Raises:
        HTTPException: If a database or other unexpected error occurs.
    """
    try:
        member = get_member_by_id(db, member_id)
        if member:
            db.delete(member)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error")
