# service/word_set_service.py

from .service import Service
from model import WordSet
from dto import UpdateWordSetDTO
from sqlalchemy.future import select

class WordSetService(Service):
    
    async def create_word_set(self, word_set: WordSet) -> WordSet:
        # word_set.user_id = 1
        self.db.add(word_set)
        await self.db.commit()
        await self.db.refresh(word_set)
        return word_set
    
    async def get_word_set(self, word_set_id: int) -> WordSet | None:
        result = await self.db.execute(select(WordSet).filter(WordSet.id == word_set_id))
        return result.scalars().first()
    
    async def get_all_word_sets_by_user(self, user_id: int) -> list[WordSet]:
        result = await self.db.execute(select(WordSet).filter(WordSet.user_id == user_id))
        return result.scalars().all()
    
    async def update_word_set(self, existing_word_set: WordSet , new_word_set: UpdateWordSetDTO) -> WordSet | None:
        fields_to_update = [field for field in UpdateWordSetDTO.model_fields if getattr(new_word_set, field) is not None]
        for field in fields_to_update:
            setattr(existing_word_set, field, getattr(new_word_set, field))
        await self.db.commit()
        await self.db.refresh(existing_word_set)
        return existing_word_set
    
    async def delete_word_set(self, word_set_id: int) -> bool:
        word_set = await self.get_word_set(word_set_id)
        if not word_set:
            return False
        self.db.delete(word_set)
        await self.db.commit()
        return True