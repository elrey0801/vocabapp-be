from config.mysql import DBMySQL
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey

class WordSet(DBMySQL.Base):
    __tablename__ = 'word_sets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    # Relationship này sẽ có cascade
    words = relationship("Word", back_populates="word_set", cascade="all, delete-orphan")