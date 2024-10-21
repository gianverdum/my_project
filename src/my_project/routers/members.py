from fastapi import APIRouter, HTTPException
from src.my_project.services.members_service import create_member, get_all_members
from src.my_project.models.member import Member

router = APIRouter()

# POST endpoint to create a new member
@router.post("/members", response_model=Member, status_code=201)
def create_member_endpoint(member: Member):
    try:
        created_member = create_member(member)
        return created_member
    except HTTPException as http_err:
        raise http_err # Propagate especified exceptions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) # General exceptions treatment

# GET endpoint to retrieve all members (for test purposes)
@router.get("/members", response_model=list[Member])
def get_members_endpoint():
    return get_all_members()
