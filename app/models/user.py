from typing import Optional
from pydantic import BaseModel
from app.api.enums.user_roles import UserRole
from app.models.base import Base, Column, String, DateTime, datetime, gen_id



class BaseUser(BaseModel):
    username: str
    password: str


class CreateUser(BaseUser):
    username: str
    password: str
    role: UserRole


    

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_id)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        # Here you would implement proper password hashing and verification
        return self.password_hash == password  # Simplified for example purposes



__all__ = ["User"]


