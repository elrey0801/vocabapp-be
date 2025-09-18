from service import WordService
from fastapi import Depends
from dto import UpdateWordDTO, CreateWordDTO
from model import Word
from exception import AppException, ErrorCode

class WordController:
    def __init__(self, word_service: WordService = Depends()):
        self.word_service = word_service
        
    async def create_word(self, word: CreateWordDTO, user_id: int) -> Word:
        new_word = Word(
            name=word.name,
            meaning=word.meaning,
            fscore=0,
            word_set_id=word.word_set_id,
            examples=word.examples or [],
            user_id=user_id
        )
        return await self.word_service.create_word(new_word)
    
    async def update_word(self, update_word: UpdateWordDTO, user_id: int) -> Word:
        existing_word = await self.word_service.get_word(update_word.id)
        if not existing_word:
            raise AppException(ErrorCode.WORD_NOT_FOUND, f"Word with ID {update_word.id} not found")
        if existing_word.user_id != user_id:
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to update this word")
        
        updated_word = await self.word_service.update_word(existing_word, update_word)
        return updated_word
    
    async def get_all_words_by_word_set(self, word_set_id: int, user_id: int) -> list[Word]:
        return await self.word_service.get_all_words_by_word_set(word_set_id, user_id)
    
    async def delete_word(self, word_id: int, user_id: int) -> bool:
        word = await self.word_service.get_word(word_id)
        if not word:
            raise AppException(ErrorCode.WORD_NOT_FOUND, f"Word with ID {word_id} not found")
        if word.user_id != user_id:
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to delete this word")
        return await self.word_service.delete_word(word_id)