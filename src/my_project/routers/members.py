from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.my_project.models.member import Member
from src.my_project.services.members_service import create_member, get_all_members, get_db, DuplicateMemberException

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
def read_members(name: str = Query(None), club: str = Query(None), db: Session = Depends(get_db)):
    return get_all_members(db, name, club)
