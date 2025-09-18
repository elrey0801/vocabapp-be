# dto/token_dto.py

from pydantic import BaseModel
from model import TokenType
from datetime import datetime
from typing import Optional

class TokenDTO(BaseModel):
    id: int
    token: str
    token_type: TokenType
    
    class Config:
        from_attributes = True

class TokenPair(BaseModel):
    access_token: TokenDTO
    refresh_token: TokenDTO