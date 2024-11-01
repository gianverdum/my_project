# src/routers/member_router.py
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.member import MemberCreate, MemberRead, MemberUpdate
from src.services.member_services import create_member, delete_member, get_member_by_id, get_members, update_member

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.post(
    "/members/",
    response_model=MemberRead,
    summary="Create a new member",
    description="This endpoint allows you to create a \
        new member in the database",
    tags=["Members"],
)
def add_member(member: MemberCreate, db: Session = Depends(get_db)) -> MemberRead:
    """
    Create a new member entry in the database.

    Args:
        member (MemberCreate): Data required to create a new member.
        db (Session, optional): Database session dependency.

    Returns:
        MemberRead: The newly created member record.

    Raises:
        HTTPException: If a database or server error occurs.
    """
    return create_member(db, member)


@router.get(
    "/members/",
    response_model=list[MemberRead],
    summary="Retrieve a list of members",
    description="Fetch a list of members with optional\
        pagination.",
    tags=["Members"],
)
def list_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[MemberRead]:
    """
    Retrieve a list of members from the database.

    Args:
        skip (int, optional): Number of records to skip \
            for pagination (default is 0).
        limit (int, optional): Maximum number of records \
            to return (default is 10).
        db (Session, optional): Database session dependency.

    Returns:
        list[MemberRead]: A list of member records.

    Raises:
        HTTPException: If a database or server error occurs.
    """
    members = get_members(db, skip=skip, limit=limit)
    return [MemberRead.model_validate(member) for member in members]


@router.get(
    "/members/{id}",
    response_model=MemberRead,
    summary="Retrieve a specific member by ID",
    description="Fetch a member's details using their\
        unique ID.",
    tags=["Members"],
)
def get_member(id: int, db: Session = Depends(get_db)) -> MemberRead:
    """
    Retrieve a specific member by ID.

    Args:
        id (int): The ID of the member to retrieve.
        db (Session, optional): Database session dependency.

    Returns:
        MemberRead: The member record if found.

    Raises:
        HTTPException: If the member is not found.
    """
    member = get_member_by_id(db, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put(
    "/members/{id}",
    response_model=MemberRead,
    summary="Update an existing member's information",
    description="Modify the details of an existing member.",
    tags=["Members"],
)
def modify_member(id: int, updated_member: MemberUpdate, db: Session = Depends(get_db)) -> MemberRead:
    """
    Update an existing member's information.

    Args:
        id (int): The ID of the member to update.
        updated_member (MemberUpdate): Data to update the member with.
        db (Session, optional): Database session dependency.

    Returns:
        MemberRead: The updated member record.

    Raises:
        HTTPException: If the member is not found.
    """
    member = update_member(db, id, updated_member)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete(
    "/members/{id}",
    status_code=204,
    summary="Delete a member",
    description="Remove a member from the database using\
        their ID.",
    tags=["Members"],
)
def remove_member(id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a member from the database.

    Args:
        id (int): The ID of the member to delete.
        db (Session, optional): Database session dependency.

    Raises:
        HTTPException: If the member is not found.
    """
    success = delete_member(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
