# model/special_word.py

# This model is design for collocation and phrasal verbs

import enum
from config.mysql import DBMySQL
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey, JSON

class WordType(enum.Enum):
    COLLOCATION = 'collocation'
    PHRASAL_VERB = 'phrasal_verb'

class SpecialWord(DBMySQL.Base):
    __tablename__ = 'special_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    meaning = Column(String(255), nullable=False)
    fscore = Column(Integer, nullable=False)
    type = Column(Enum(WordType), nullable=False)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    examples = Column(JSON, nullable=True, default=list)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    word = relationship("Word", back_populates="special_words")
    user = relationship("User", back_populates="special_words")