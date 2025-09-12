# dto/word_set_dto.py

from pydantic import BaseModel, Field

class WordSetDTO(BaseModel):
    id: int | None = Field(None, description="ID of the word set")
    name: str = Field(..., description="Name of the word set")
    description: str | None = Field(None, description="Description of the word set")
    
    class Config:
        from_attributes = True
    
class UpdateWordSetDTO(BaseModel):
    id: int = Field(..., description="ID of the word set")
    name: str | None = Field(None, description="Name of the word set")
    description: str | None = Field(None, description="Description of the word set")
    
    class Config:
        from_attributes = True