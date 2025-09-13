# model/user.py

import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from config.mysql import DBMySQL
from datetime import datetime, timezone

ROLE_PRIORITY_MAP = {
    "admin": 3,
    "user": 2,
    "trial_user": 1,
}


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    TRIAL_USER = "trial_user"

    @property
    def priority(self):
        return ROLE_PRIORITY_MAP[self.value]
    
    def __lt__(self, other: 'Role'):
        if self.__class__ is other.__class__:
            return self.priority < other.priority
        return NotImplemented
    
    def __le__(self, other: 'Role'):
        if self.__class__ is other.__class__:
            return self.priority <= other.priority
        return NotImplemented
    
    def __gt__(self, other: 'Role'):
        if self.__class__ is other.__class__:
            return self.priority > other.priority
        return NotImplemented
    
    def __ge__(self, other: 'Role'):
        if self.__class__ is other.__class__:
            return self.priority >= other.priority
        return NotImplemented

class User(DBMySQL.Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    private_key = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.TRIAL_USER, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    word_sets = relationship("WordSet", back_populates="user", cascade="all, delete-orphan")
    special_words = relationship("SpecialWord", back_populates="user", cascade="all, delete-orphan")
    words = relationship("Word", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")