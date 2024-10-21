from fastapi import HTTPException
from src.my_project.models.member import Member

# List to store members
members_db = []

def create_member(member: Member):
    # Verify if member exists comparing phone
    if any(m["phone"] == member.phone for m in members_db):
        raise HTTPException(status_code=409, detail="Member with this phone number already exists.")

    new_id = len(members_db) + 1 #ID increment
    member_with_id = member.model_dump() # Use Dict to get user data
    member_with_id['id'] = new_id # Add ID to member
    members_db.append(member_with_id) # Add new member to the list
    return member_with_id

def get_all_members():
    return members_db
