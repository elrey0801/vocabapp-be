# service/service.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql import DBMySQL


class Service:
    def __init__(self, db: AsyncSession = Depends(DBMySQL.get_async_db)):
        self.db = db