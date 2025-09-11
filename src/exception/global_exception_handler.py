# exceptions/global_exception_handler.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception.app_exception import AppException
from exception.error_code import ErrorCode
from config.logger import logger

class GlobalExceptionHandler:
    @staticmethod
    async def app_exception_handler(request: Request, exc: AppException):
        error_info = exc.error_code.value
        error_path = exc.error_path
        message = exc.args[0] if exc.args else error_info.message
        logger.error(f"path: {error_path}, message: {message}, error_code: {error_info.code}")
        return JSONResponse(
            status_code = error_info.status_code,
            content={"message": exc.return_message, "error_code": error_info.code}
        )
    @staticmethod
    async def other_exception_handler(request: Request, exc: Exception):
        error_info = ErrorCode.UNCATEGORIZED_EXCEPTION.value
        message = exc.args[0] if exc.args else error_info.message
        logger.error(f"message: {message}, error_code: {error_info.code}")
        return JSONResponse(
            status_code = error_info.status_code,
            content={"message": message, "error_code": error_info.code}
        )

def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, GlobalExceptionHandler.app_exception_handler)
    app.add_exception_handler(Exception, GlobalExceptionHandler.other_exception_handler)