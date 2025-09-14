# controller/user_controller.py

from service import UserService
from fastapi import Depends
from dto import CreateUserDTO, UserDTO
from model import User
import secrets, bcrypt
from exception import AppException, ErrorCode
from config import logger

class UserController:
    def __init__(self, user_service: UserService = Depends()):
        self.user_service = user_service
        
    async def create_user(self, user: CreateUserDTO) -> UserDTO:
        if await self.user_service.get_user_by_username(user.username):
            raise AppException(
                error_code=ErrorCode.USER_EXISTED, 
                alt_message=f"User with username {user.username} already exists"
            )
        
        if await self.user_service.get_user_by_email(user.email):
            raise AppException(
                error_code=ErrorCode.USER_EXISTED, 
                alt_message=f"User with email {user.email} already exists"
            )
        
        if await self.user_service.get_user_by_phone(user.phone):
            raise AppException(
                error_code=ErrorCode.USER_EXISTED, 
                alt_message=f"User with phone {user.phone} already exists"
            )
        
        private_key = secrets.token_hex(32)
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(**user.model_dump())
        new_user.private_key = private_key

        created_user = await self.user_service.create_user(new_user)
        logger.info(f"User created [id={created_user.id}, username={created_user.username}]")
        return UserDTO.model_validate(created_user)
    
    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        user = await self.user_service.get_user_by_id(user_id)
        if user:
            return UserDTO.model_validate(user)
        return None
    
    async def get_user_by_username(self, username: str) -> UserDTO | None:
        user = await self.user_service.get_user_by_username(username)
        if user:
            return UserDTO.model_validate(user)
        return None

    async def update_user_password(self, username: str, old_password: str, new_password: str) -> bool:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            raise AppException(
                error_code=ErrorCode.USER_NOT_FOUND, 
                alt_message=f"User with username {username} not found"
            )
        
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            raise AppException(
                error_code=ErrorCode.INVALID_CREDENTIALS, 
                alt_message="Old password is incorrect"
            )
        
        if old_password == new_password:
            raise AppException(
                error_code=ErrorCode.INVALID_REQUEST, 
                alt_message="New password must be different from old password"
            )
        
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = new_hashed_password
        await self.user_service.update_user(user)
        logger.info(f"User password updated [id={user.id}, username={user.username}]")
        return True
    
    async def reset_user_password(self, username: str) -> str:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            raise AppException(
                error_code=ErrorCode.USER_NOT_FOUND, 
                alt_message=f"User with username {username} not found"
            )
        
        new_password = secrets.token_urlsafe(12)
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = new_hashed_password
        await self.user_service.update_user(user)
        logger.info(f"User password reset [id={user.id}, username={user.username}]")
        return new_password
    
    async def delete_user(self, username: str) -> bool:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            raise AppException(
                error_code=ErrorCode.USER_NOT_FOUND, 
                alt_message=f"User with username {username} not found"
            )
        
        result = await self.user_service.delete_user(user)
        if result:
            logger.info(f"User deleted [id={user.id}, username={user.username}]")
        return result