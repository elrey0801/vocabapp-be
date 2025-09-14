# service/word_service.py

from .service import Service
from model import Word
from dto import UpdateWordDTO

class WordService(Service):
    async def create_word(self, word: Word) -> Word:
        self.db.add(word)
        await self.db.commit()
        await self.db.refresh(word)
        return word
    
    async def get_word(self, word_id: int) -> Word | None:
        return await self.db.query(Word).filter(Word.id == word_id).first()
    
    async def update_word(self, new_word: Word) -> Word:
        existing_word = await self.get_word(new_word.id)
        if not existing_word:
            return None
        fields_to_update = [field for field in UpdateWordDTO.model_fields if getattr(new_word, field) is not None]
        for field in fields_to_update:
            setattr(existing_word, field, getattr(new_word, field))
        await self.db.commit()
        await self.db.refresh(existing_word)
        return existing_word
    
    async def delete_word(self, word_id: int) -> bool:
        word = await self.get_word(word_id)
        if not word:
            return False
        await self.db.delete(word)
        await self.db.commit()
        return True