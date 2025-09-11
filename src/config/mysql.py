# config/mysql.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from config.env_config import settings
from config.logger import logger


DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

class DBMySQL:
    engine = None
    Base = declarative_base()
    SessionLocal = None

    def __new__(cls):
        return None

    @classmethod
    def connect(cls):
        try:
            cls.engine = create_engine(DATABASE_URL, echo=False)
            if not database_exists(cls.engine.url):
                create_database(cls.engine.url)
                logger.info('New DB_MySQL created')
            else:
                cls.engine.connect()
                logger.info('Connect DB_MySQL:: OK')
        except Exception as error:
            logger.error('Connect DB_MySQL:: Failed')
            logger.error(error)

        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
    
    @classmethod
    def close(cls):
        if cls.engine:
            cls.engine.dispose()
            logger.info('Close DB_MySQL connection')

    @classmethod
    def get_db(cls):
        db = cls.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# DBMySQL.connect()
