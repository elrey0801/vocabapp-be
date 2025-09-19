# controller/auth_controller.py

from exception import ErrorCode, AppException
from service import TokenService, UserService
from fastapi import Depends
from model import User, Token, TokenType
import bcrypt, jwt
from datetime import datetime, timezone, timedelta
from config import settings, logger
from dto import TokenPair, TokenDTO

class AuthController:
    def __init__(self, token_service: TokenService = Depends(), user_service: UserService = Depends()):
        self.token_service = token_service
        self.user_service = user_service

    async def create_token(self, user: User, token_type: TokenType) -> Token:
        await self.user_service.db.refresh(user)  # Ensure user is up-to-date to avoid stale data issues
        created_at=datetime.now(timezone.utc)
        # logger.debug(f"user id = {user.id}, token_type = {token_type}")
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

    async def login(self, username: str, password: str) -> TokenPair:
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
        
        if not user.is_active:
            raise AppException(
                error_code=ErrorCode.USER_NOT_ACTIVATED, 
                alt_message=f"User {username} is inactive",
                return_message="User account is inactive"
            )
        
        return await self.create_token_pair(user)
        

    async def create_token_pair(self, user: User) -> TokenPair:
        access_token: Token = await self.create_token(user, TokenType.ACCESS)
        refresh_token: Token = await self.create_token(user, TokenType.REFRESH)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)


    async def verify_token(self, token: TokenDTO) -> bool:
        token_db = await self.token_service.get_token_by_id(token.id)
        if not token_db:
            raise AppException(
                error_code=ErrorCode.TOKEN_NOT_FOUND, 
                alt_message=f"Token ({token.token_type}) with id={token.id} not found",
                return_message="Invalid token"
            )
        if token_db.token != token.token or token_db.token_type != token.token_type:
            raise AppException(
                error_code=ErrorCode.INVALID_TOKEN, 
                alt_message=f"Invalid {token.token_type} token",
                return_message="Invalid token"
            )
        if token_db.is_revoked:
            raise AppException(
                error_code=ErrorCode.TOKEN_REVOKED, 
                alt_message=f"Token ({token.token_type}) with id={token.id} revoked",
                return_message="Invalid token"
            )

        user_db = await self.user_service.get_user_by_id(token_db.user_id)

        try:
            jwt.decode(token.token, user_db.private_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            await self.revoke_token(token)
            return False
        except jwt.InvalidTokenError:
            raise AppException(
                error_code=ErrorCode.INVALID_TOKEN, 
                alt_message=f"Invalid {token.token_type} token",
                return_message="Invalid token"
            )
        
        return True
    
    async def revoke_token(self, token: TokenDTO) -> bool:
        token_db = await self.token_service.get_token_by_id(token.id)
        if not token_db:
            raise AppException(
                error_code=ErrorCode.TOKEN_NOT_FOUND,
                alt_message=f"Token with id={token.id} not found",
                return_message="Invalid token"
            )
        
        if token_db.token != token.token or token_db.token_type != token.token_type:
            raise AppException(
                error_code=ErrorCode.INVALID_TOKEN, 
                alt_message=f"Invalid {token.token_type} token",
                return_message="Invalid token"
            )

        token_db.is_revoked = True
        await self.token_service.update_token(token_db)
        logger.info(f"Token with id={token_db.id} revoked")
        return True