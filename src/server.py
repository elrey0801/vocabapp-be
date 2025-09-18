# server.py
from config import settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, log_config=None, workers=settings.APP_WORKERS)