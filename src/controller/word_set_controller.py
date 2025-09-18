# controller/word_set_controller.py

from model import WordSet
from service import WordSetService
from fastapi import APIRouter, HTTPException, Depends
from config import logger
from exception import AppException, ErrorCode
from config import DBMySQL
from dto import UpdateWordSetDTO

class WordSetController:
    def __init__(self, word_set_service: WordSetService = Depends()):
        self.word_set_service = word_set_service
        
    async def create_word_set(self, name: str, description: str = None) -> WordSet:
        return await self.word_set_service.create_word_set(WordSet(name=name, description=description, user_id=1))
    
    async def update_word_set(self, update_word_set: UpdateWordSetDTO, user_id: int) -> WordSet:
        existing_word_set = await self.word_set_service.get_word_set(update_word_set.id)
        if not existing_word_set:
            raise AppException(ErrorCode.WORD_SET_NOT_FOUND, f"Word set with ID {update_word_set.id} not found")
        if existing_word_set.user_id != user_id:
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to update this word set")
        
        updated_word_set = await self.word_set_service.update_word_set(existing_word_set, update_word_set)
        return updated_word_set
    
    async def get_all_word_sets_by_user(self, user_id: int) -> list[WordSet]:
        return await self.word_set_service.get_all_word_sets_by_user(user_id)
    
    async def delete_word_set(self, word_set_id: int, user_id: int) -> bool:
        word_set = await self.word_set_service.get_word_set(word_set_id)
        if not word_set:
            raise AppException(ErrorCode.WORD_SET_NOT_FOUND, f"Word set with ID {word_set_id} not found")
        if word_set.user_id != user_id:
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to delete this word set")
        return await self.word_set_service.delete_word_set(word_set_id)
    
    