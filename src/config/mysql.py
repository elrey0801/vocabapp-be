# config/mysql.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from config import settings, logger


# Keep sync URL only for database creation/checking
SYNC_DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
ASYNC_DATABASE_URL = f"mysql+aiomysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

class DBMySQL:
    _sync_engine = None  # Only for database creation
    async_engine = None
    Base = declarative_base()
    AsyncSessionLocal = None

    def __new__(cls):
        return None

    @classmethod
    def connect(cls):
        try:
            # Sync engine only for database creation/checking
            cls._sync_engine = create_engine(
                SYNC_DATABASE_URL, 
                echo=False,
                connect_args={
                    "charset": "utf8mb4",
                    "autocommit": False,
                    "use_pure": False
                }
            )
            
            # Async engine for actual operations
            cls.async_engine = create_async_engine(
                ASYNC_DATABASE_URL,
                echo=False,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_timeout=30,
                connect_args={
                    "charset": "utf8mb4",
                    "autocommit": False
                }
            )
            
            # Database creation check using sync engine
            if not database_exists(cls._sync_engine.url):
                create_database(cls._sync_engine.url)
                logger.info('New DB_MySQL created')
            else:
                cls._sync_engine.connect()
                logger.info('Connect DB_MySQL:: OK')
                
            # Only create async session
            cls.AsyncSessionLocal = async_sessionmaker(
                bind=cls.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            )
        except Exception as error:
            logger.error('Connect DB_MySQL:: Failed')
            logger.error(error)
    
    @classmethod
    async def close(cls):
        if cls._sync_engine:
            cls._sync_engine.dispose()
        if cls.async_engine:
            await cls.async_engine.dispose()
        logger.info('Close DB_MySQL connection')
            
    @classmethod
    async def get_async_db(cls):
        async with cls.AsyncSessionLocal() as db:
            try:
                yield db
            finally:
                await db.close()

# DBMySQL.connect()
