# models/token.py

import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.mysql import DBMySQL
from datetime import datetime, timezone

class TokenType(enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class Token(DBMySQL.Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_type = Column(Enum(TokenType))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="tokens")