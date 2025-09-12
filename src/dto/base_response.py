# dto/base_response.py

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    message: Optional[str] = "OK"
    body: T = []