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