import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.my_project.schemas.member import Member, MemberDB
from src.my_project.services.members_service import (
    create_member,
    delete_member,
    get_all_members,
    get_db,
    DuplicateMemberException,
    get_member_by_id,
    update_member_service
)

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)


# POST endpoint to create a new member
@router.post("/members", response_model=Member, status_code=201)
def add_member(member: Member, db: Session = Depends(get_db)):
    logger.info(f"Adding new member: {member}")
    try:
        created_member = create_member(member, db)
        logger.info(f"Member created successfully: {created_member}")
        return created_member
    except DuplicateMemberException:
        logger.warning(f"Duplicate member attempt: {member}")
        raise HTTPException(status_code=409, detail="Member already exists")
    except HTTPException as e:
        logger.error(f"HTTP exception occurred: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET endpoint to retrieve all members by filtering
@router.get("/members", response_model=list[Member])
def read_members(
    name: str = Query(None),
    club: str = Query(None),
    phone: str = Query(None),
    db: Session = Depends(get_db)
):
    logger.info("Retrieving members with filters "
                "- Name: %s, Club: %s, Phone: %s", name, club, phone)
    return get_all_members(db, name, phone, club)


# GET /members/{id} endpoint to retrieve a member by ID
@router.get("/members/{id}", response_model=Member)
def read_member_by_id(id: int, db: Session = Depends(get_db)):
    logger.info(f"Retrieving member by ID: {id}")
    member = get_member_by_id(id, db)
    if member is None:
        logger.warning(f"Member not found: ID {id}")
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# PUT endpoint to update members
@router.put("/members/{id}", response_model=MemberDB)
def update_member(
    id: int,
    member_update: Member,
    db: Session = Depends(get_db)
):
    logger.info(f"Updating member ID: {id} with data: {member_update}")
    updated_member = update_member_service(db, id, member_update)

    if not updated_member:
        logger.warning(f"Member not found for update: ID {id}")
        raise HTTPException(status_code=404, detail="Member not found")

    logger.info(f"Member updated successfully: {updated_member}")
    return updated_member


# DELETE endpoint
@router.delete("/members/{id}", response_description="Delete a member")
def delete_member_endpoint(id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting member ID: {id}")
    success = delete_member(id, db)
    if not success:
        logger.warning(f"Member not found for deletion: ID {id}")
        raise HTTPException(status_code=404, detail="Member not found")

    logger.info(f"Member deleted successfully: ID {id}")
    return {"message": "Member deleted successfully"}
