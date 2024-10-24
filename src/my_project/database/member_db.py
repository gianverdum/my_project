from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Base class for the SQLAlchemy models
Base = declarative_base()


# SQLAlchemy model for the 'members' table
class MemberDB(Base):
    __tablename__ = 'members'

    # Columns that represent fields in the 'members' table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    club = Column(String)

    # Method to convert the object to a dictionary format
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "club": self.club,
        }
