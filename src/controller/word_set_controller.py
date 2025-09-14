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
    
    async def update_word_set(self, word_set_id: int, name: str = None, description: str = None) -> WordSet:
        update_dto = UpdateWordSetDTO(id=word_set_id, name=name, description=description)
        updated_word_set = await self.word_set_service.update_word_set(update_dto)
        if not updated_word_set:
            raise AppException(ErrorCode.WORD_SET_NOT_FOUND, f"Word set with ID {word_set_id} not found")
        return updated_word_set
    
    