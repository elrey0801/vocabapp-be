# config/env_config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from config.logger import logger
 
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PDDA2-API")
    APP_WORKERS: int = int(os.getenv("APP_WORKERS", 1))
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")

    PORT: int = int(os.getenv("PORT", 8888))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    ENV: str = os.getenv("ENV", "dev")
    ORIGINS: str = os.getenv("ORIGINS", "*")
    
    ACCESS_TOKEN_MAX_AGE: int = int(os.getenv("ACCESS_TOKEN_MAX_AGE", 60*60))
    REFRESH_TOKEN_MAX_AGE: int = int(os.getenv("REFRESH_TOKEN_MAX_AGE", 60*60*24*7))
    
    AI_API_KEY: str = os.getenv("AI_API_KEY", "No AI API KEY")

    OPEN_USER_REGISTRATION: bool = os.getenv("OPEN_USER_REGISTRATION", 0) == 1
    PRODUCTION_MODE: bool = os.getenv("PRODUCTION_MODE", 0) == 1

    class Config:
        env_file = ".env"

    def print_settings(self):
        if not self.PRODUCTION_MODE:
            logger.info("CURRENT SETTINGS:")
            for key, value in settings.model_dump().items():
                logger.info(f"{key}: {value}")
        else:
            logger.info("CURRENT SETTINGS:")
            logger.info(f"{"APP_WORKERS"}: {self.APP_WORKERS}")
            logger.info(f"{"DB_HOST"}: {self.DB_HOST}")
            logger.info(f"{"DB_MONGO_HOST"}: {self.DB_MONGO_HOST}")
            logger.info(f"{"PORT"}: {self.PORT}")
        

settings = Settings()