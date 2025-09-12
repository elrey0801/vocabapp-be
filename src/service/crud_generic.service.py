# service/crud_generic.service.py

# currently not in use

from .service import Service
from typing import TypeVar, Generic
from model import *

T = TypeVar('T')

class CRUDGenericService(Service, Generic[T]):
    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get(self, obj_id: int) -> T | None:
        return self.db.query(T).filter(T.id == obj_id).first()
    
    def update(self, new_obj: T) -> T | None:
        existing_obj = self.get(new_obj.id)
        if not existing_obj:
            return None
        for attr, value in vars(new_obj).items():
            setattr(existing_obj, attr, value)
        self.db.commit()
        self.db.refresh(existing_obj)
        return existing_obj
    
    def delete(self, obj_id: int) -> bool:
        obj = self.get(obj_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True