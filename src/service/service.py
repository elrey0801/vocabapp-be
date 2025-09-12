# service/service.py
from fastapi import Depends
from sqlalchemy.orm import Session
from config.mysql import DBMySQL


class Service:
    def __init__(self, db: Session = Depends(DBMySQL.get_db)):
        self.db = db