# app.py

from fastapi import FastAPI
from config import *
# from routers import *

from exception.global_exception_handler import configure_exception_handlers
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    DBMySQL.connect()
    DBMySQL.Base.metadata.create_all(bind=DBMySQL.engine)
    logger.info(f'App started successfully on port = {settings.PORT}, host = {settings.HOST}')

    
    yield  # App running
    
    # Shutdown
    logger.info('App shutting down')
    DBMySQL.close()



app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan, docs_url=None, redoc_url=None)
Logger.setup_logging()


origins = settings.ORIGINS.split(",") if settings.ORIGINS != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings.print_settings()

configure_exception_handlers(app)





