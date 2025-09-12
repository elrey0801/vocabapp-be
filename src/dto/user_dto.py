# dto/user_dto.py

from pydantic import BaseModel, Field

class UpdateUserDTO(BaseModel):
    username: str = Field(..., description="The user's username")
    password: str | None = Field(None, description="The user's password")
    email: str | None = Field(None, description="The user's email address")
    phone: str | None = Field(None, description="The user's phone number")
    private_key: str | None = Field(None, description="The user's private key")
    
    class Config:
        from_attributes = True