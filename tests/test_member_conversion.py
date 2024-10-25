# src/my_project/tests/test_member_conversion.py
from src.my_project.models.models import Member as ORMMember
from src.my_project.schemas.member import MemberSchema as PydanticMember


# Use pytest to indicate this is a test module
def test_member_conversion():
    # Create a mock ORM instance
    orm_instance = ORMMember(
        id=1, name="John Doe", phone="12345678901", club="Sample Club"
    )

    # Convert the ORM instance to a Pydantic model instance
    pydantic_member = PydanticMember.model_validate(orm_instance)

    # Assert that the fields match
    assert pydantic_member.id == orm_instance.id
    assert pydantic_member.name == orm_instance.name
    assert pydantic_member.phone == orm_instance.phone
    assert pydantic_member.club == orm_instance.club
