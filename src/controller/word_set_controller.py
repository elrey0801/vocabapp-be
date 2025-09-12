# controller/word_set_controller.py

from model import WordSet
from service import WordSetService
from fastapi import APIRouter, HTTPException, Depends
from config import logger
from exception.app_exception import AppException
from config import DBMySQL
from sqlalchemy.orm import Session

class WordSetController:
    def __init__(self, word_set_service: WordSetService = Depends(), db: Session = Depends(DBMySQL.get_db)):
        self.db = db
        self.word_set_service = word_set_service
        
    def create_word_set(self, name: str, description: str = None) -> WordSet:
        return self.word_set_service.create_word_set(WordSet(name=name, description=description))
    