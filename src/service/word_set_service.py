# service/word_set_service.py

from .service import Service
from model import WordSet
from dto import UpdateWordSetDTO

class WordSetService(Service):
    def create_word_set(self, word_set: WordSet) -> WordSet:
        # word_set.user_id = 1
        self.db.add(word_set)
        self.db.commit()
        self.db.refresh(word_set)
        return word_set
    
    def get_word_set(self, word_set_id: int) -> WordSet | None:
        return self.db.query(WordSet).filter(WordSet.id == word_set_id).first()
    
    def update_word_set(self, new_word_set: UpdateWordSetDTO) -> WordSet | None:
        existing_word_set = self.get_word_set(new_word_set.id)
        if not existing_word_set:
            return None
        fields_to_update = [field for field in UpdateWordSetDTO.model_fields if getattr(new_word_set, field) is not None]
        for field in fields_to_update:
            setattr(existing_word_set, field, getattr(new_word_set, field))
        self.db.commit()
        self.db.refresh(existing_word_set)
        return existing_word_set
    
    def delete_word_set(self, word_set_id: int) -> bool:
        word_set = self.get_word_set(word_set_id)
        if not word_set:
            return False
        self.db.delete(word_set)
        self.db.commit()
        return True