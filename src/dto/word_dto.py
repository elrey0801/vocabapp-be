# dto/word_dto.py

from pydantic import BaseModel, Field

class WordDTO(BaseModel):
    id: int | None = Field(None, description="ID of the word")
    word_set_id: int = Field(..., description="ID of the associated word set")
    name: str = Field(..., description="Name of the word")
    meaning: str = Field(..., description="Meaning of the word")
    fscore: int = Field(..., description="Familiarity score of the word")
    examples: list[str] | None = Field(None, description="Example sentences for the word")
    user_id: int | None = Field(..., description="ID of the associated user")
    
    class Config:
        from_attributes = True

class UpdateWordDTO(BaseModel):
    id: int = Field(..., description="ID of the word")
    word_set_id: int | None = Field(None, description="ID of the associated word set")
    name: str | None = Field(None, description="Name of the word")
    meaning: str | None = Field(None, description="Meaning of the word")
    fscore: int | None = Field(None, description="Familiarity score of the word")
    examples: list[str] | None = Field(None, description="Example sentences for the word")
    
    class Config:
        from_attributes = True