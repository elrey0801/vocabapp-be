# dto/token_dto.py

from pydantic import BaseModel
from model import TokenType

class TokenDTO(BaseModel):
    id: int
    token: str
    user_id: int
    token_type: TokenType
    created_at: str
    
    class Config:
        from_attributes = True

class TokenPair(BaseModel):
    access_token: TokenDTO
    refresh_token: TokenDTO