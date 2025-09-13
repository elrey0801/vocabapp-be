# service/user_service.py

from model import User
from exception import ErrorCode, AppException
from config import logger
from .service import Service
from dto import UpdateUserDTO

class UserService(Service):
    async def create_user(self, user: User) -> User:
        await self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
        
    async def get_all_users(self) -> list[User]:
        return await self.db.query(User).all()
    
    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.db.query(User).filter(User.id == user_id).first()
        return user
    
    async def get_user_by_username(self, username: str) -> User:
        user = await self.db.query(User).filter(User.username == username).first()
        return user
    
    async def update_user(self, new_user: UpdateUserDTO) -> User:
        existing_user = await self.get_user_by_username(new_user.username)
        if not existing_user:
            raise AppException(ErrorCode.USER_NOT_FOUND, f"User with username {new_user.username} not found")
        
        fields_to_update = [field for field in UpdateUserDTO.model_fields if getattr(new_user, field) is not None]
        for field in fields_to_update:
            setattr(existing_user, field, getattr(new_user, field))
                
        await self.db.commit()
        await self.db.refresh(existing_user)
        return existing_user
    
    async def delete_user(self, user: User) -> bool:
        user = await self.get_user_by_id(user.id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True