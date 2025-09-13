# controller/token_controller.py

from exception import ErrorCode, AppException
from service import TokenService, UserService
from fastapi import Depends
from model import User, Token, TokenType
import bcrypt, jwt
from datetime import datetime, timezone, timedelta
from config import settings, logger

class TokenController:
    def __init__(self, token_service: TokenService = Depends(), user_service: UserService = Depends()):
        self.token_service = token_service
        self.user_service = user_service

    async def create_token(self, user: User, token_type: TokenType) -> Token:
        created_at=datetime.now(timezone.utc)
        token_payload = {
            "user_id": user.id,
            "exp": created_at + (timedelta(seconds=settings.ACCESS_TOKEN_MAX_AGE) 
                                if token_type == TokenType.ACCESS 
                                else timedelta(seconds=settings.REFRESH_TOKEN_MAX_AGE)),
            "token_type": TokenType.ACCESS.value if token_type == TokenType.ACCESS else TokenType.REFRESH.value
        }

        token = Token(
            token=jwt.encode(token_payload, user.private_key, algorithm="HS256"),
            user_id=user.id,
            token_type=TokenType.ACCESS if token_type == TokenType.ACCESS else TokenType.REFRESH,
            created_at=created_at
        )
        return await self.token_service.create_token(token)


    async def create_token_pair(self, username: str, password: str) -> str:
        user: User = await self.user_service.get_user_by_username(username)
        if not user:
            raise AppException(
                error_code=ErrorCode.INVALID_CREDENTIALS, 
                alt_message=f"User with username {username} not found",
                return_message="Invalid username or password"
            )
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise AppException(
                error_code=ErrorCode.INVALID_CREDENTIALS, 
                alt_message=f"Invalid password for user {username}",
                return_message="Invalid username or password"
            )

        access_token: Token = await self.create_token(user, TokenType.ACCESS)
        refresh_token: Token = await self.create_token(user, TokenType.REFRESH)