# service/word_set_service.py

from .service import Service
from model import WordSet

class WordSetService(Service):
    def create_word_set(self, word_set: WordSet) -> WordSet:
        self.db.add(word_set)
        self.db.commit()
        self.db.refresh(word_set)
        return word_set
    
    def get_word_set(self, word_set_id: int) -> WordSet | None:
        return self.db.query(WordSet).filter(WordSet.id == word_set_id).first()
    
    def update_word_set(self, new_word_set: WordSet) -> WordSet | None:
        existing_word_set = self.get_word_set(new_word_set.id)
        if not existing_word_set:
            return None
        for attr, value in vars(new_word_set).items():
            setattr(existing_word_set, attr, value)
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