from config.mysql import DBMySQL
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey, JSON

class Word(DBMySQL.Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    meaning = Column(String(255), nullable=False)
    fscore = Column(Integer, nullable=False)
    word_set_id = Column(Integer, ForeignKey('word_sets.id'), nullable=True)
    examples = Column(JSON, nullable=True, default=list)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    word_set = relationship("WordSet", back_populates="words")

    collocations = relationship("Collocation", back_populates="word", cascade="all, delete-orphan")
    phrasal_verbs = relationship("PhrasalVerb", back_populates="word", cascade="all, delete-orphan")



