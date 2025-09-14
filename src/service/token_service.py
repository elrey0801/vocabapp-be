# service/token_service.py

from .service import Service
from model import User, Token, TokenType
from datetime import datetime, timezone, timedelta
import jwt
from config import settings

class TokenService(Service):

    async def create_token(self, token: Token) -> Token:
        self.db.add(token)
        await self.db.commit()
        return token
    
    async def get_token_by_id(self, token_id: int) -> Token:
        return await self.db.query(Token).filter(Token.id == token_id).first()
    
    async def update_token(self, token: Token) -> Token:
        await self.db.merge(token)
        await self.db.commit()
        return token
