# dto/user_dto.py

from pydantic import BaseModel, Field
from datetime import datetime
from model import Role

class UserDTO(BaseModel):
    id: int
    username: str
    email: str | None
    phone: str | None
    is_active: bool
    role: Role
    created_at: datetime
    
    class Config:
        from_attributes = True

class CreateUserDTO(BaseModel):
    username: str = Field(..., description="The user's username")
    password: str = Field(..., description="The user's password")
    email: str = Field(..., description="The user's email address")
    phone: str = Field(..., description="The user's phone number")
    
    class Config:
        from_attributes = True

class UpdateUserDTO(BaseModel):
    username: str = Field(..., description="The user's username")
    password: str | None = Field(None, description="The user's password")
    email: str | None = Field(None, description="The user's email address")
    phone: str | None = Field(None, description="The user's phone number")
    
    class Config:
        from_attributes = True