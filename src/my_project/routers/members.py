from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..schemas.member import Member, MemberDB
from ..services.members_service import (
    create_member,
    delete_member,
    get_all_members,
    get_db,
    DuplicateMemberException,
    get_member_by_id,
    update_member_service,
    delete_member
)

router = APIRouter()

# POST endpoint to create a new member
@router.post("/members", response_model=Member, status_code=201)
def add_member(member: Member, db: Session = Depends(get_db)):
    try:
        created_member = create_member(member, db)
        return created_member  # Directly return the created member
    except DuplicateMemberException:
        raise HTTPException(status_code=409, detail="Member already exists")
    except HTTPException as e:
        raise e  # Re-raise any other HTTP exceptions


# GET endpoint to retrieve all members by filtering
@router.get("/members", response_model=list[Member])
def read_members(
    name: str = Query(None),
    club: str = Query(None),
    phone: str = Query(None),
    db: Session = Depends(get_db)):
    return get_all_members(db, name, phone, club)

# GET /members/{id} endpoint to retrieve a member by ID
@router.get("/members/{id}", response_model=Member)
def read_member_by_id(id: int, db: Session = Depends(get_db)):
    member = get_member_by_id(id, db)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# PUT endpoint to update members
@router.put("/members/{id}", response_model=MemberDB)
def update_member(id: int, member_update: Member, db: Session = Depends(get_db)):
    """
    Update an exixting member by ID.
    :param id: The ID of the member to be updated.
    :param member_update: The new data for the member.
    :param db: Database session dependency.
    :return: Updated member data.
    """

    updated_member = update_member_service(db, id, member_update)

    if not updated_member:
        raise HTTPException(status_code=404, detail="Member not found")

    return updated_member

# DELETE endpoint
@router.delete("/members/{id}", response_description="Delete a member")
def delete_member_endpoint(id: int, db: Session = Depends(get_db)):
    success = delete_member(id, db) # Pass the session to delete_member function
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}
