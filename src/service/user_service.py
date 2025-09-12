# service/user_service.py

from model import User
from exception import ErrorCode, AppException
from config import logger
from .service import Service
from dto import UpdateUserDTO

class UserService(Service):
    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
        
    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        return user
    
    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        return user
    
    def update_user(self, new_user: UpdateUserDTO) -> User:
        existing_user = self.get_user_by_username(new_user.username)
        if not existing_user:
            raise AppException(ErrorCode.USER_NOT_FOUND, f"User with username {new_user.username} not found")
        
        fields_to_update = [field for field in UpdateUserDTO.model_fields if getattr(new_user, field) is not None]
        for field in fields_to_update:
            setattr(existing_user, field, getattr(new_user, field))
                
        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user
    
    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()