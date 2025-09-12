# exceptions/error_code.py

from enum import Enum
from fastapi import status

class ErrorInfo:
    def __init__(self, code, message, status_code) -> None:
        self.__code = code
        self.__message = message
        self.__status_code = status_code
    
    @property
    def code(self):
        return self.__code
    
    @property
    def message(self):
        return self.__message
    
    @property
    def status_code(self):
        return self.__status_code

class ErrorCode(Enum):
    UNCATEGORIZED_EXCEPTION = ErrorInfo(9000, "Uncategorized exception", status.HTTP_500_INTERNAL_SERVER_ERROR)
    DATABASE_ERROR = ErrorInfo(9001, "Database error exception", status.HTTP_500_INTERNAL_SERVER_ERROR)
    KEY_INVALID = ErrorInfo(9999, "Invalid error key", status.HTTP_500_INTERNAL_SERVER_ERROR)
    USER_EXISTED = ErrorInfo(4001, "User existed!", status.HTTP_400_BAD_REQUEST)
    USER_NOT_FOUND = ErrorInfo(4002, "User not found!", status.HTTP_404_NOT_FOUND)
    USERNAME_INVALID = ErrorInfo(4003, "username have to be {min}-{max} characters", status.HTTP_400_BAD_REQUEST)
    PASSWORD_INVALID = ErrorInfo(4004, "password must be at least {min} characters", status.HTTP_400_BAD_REQUEST)
    INVALID_CREDENTIALS = ErrorInfo(4005, "Invalid credentials", status.HTTP_401_UNAUTHORIZED)
    FORBIDDEN = ErrorInfo(4006, "You don't have permission to access this resource", status.HTTP_403_FORBIDDEN)
    USER_NOT_ACTIVATED = ErrorInfo(4007, "User is not active", status.HTTP_401_UNAUTHORIZED)

    
    INVALID_HEADER_USERNAME = ErrorInfo(4007, "Invalid header username", status.HTTP_401_UNAUTHORIZED)
    INACTIVATED_USER = ErrorInfo(4008, "User has not been activated, or has been blocked", status.HTTP_401_UNAUTHORIZED)
    USERNAME_CANNOT_BE_CHANGED = ErrorInfo(4009, "Username cannot be changed", status.HTTP_400_BAD_REQUEST)
    INVALID_PASSWORD = ErrorInfo(4010, "Invalid password", status.HTTP_401_UNAUTHORIZED)
    TOKEN_NOT_FOUND = ErrorInfo(4011, "Token not found", status.HTTP_401_UNAUTHORIZED)
    INVALID_TOKEN = ErrorInfo(4012, "Invalid token", status.HTTP_401_UNAUTHORIZED)
    TOKEN_EXPIRED = ErrorInfo(4013, "Token expired", status.HTTP_401_UNAUTHORIZED)
    TOKEN_REVOKED = ErrorInfo(4014, "Token revoked", status.HTTP_401_UNAUTHORIZED)
    INVALID_API_TOKEN = ErrorInfo(4015, "Invalid API token", status.HTTP_401_UNAUTHORIZED)
    PERMISSION_DENIED = ErrorInfo(4016, "Permission denied", status.HTTP_403_FORBIDDEN)

    INVALID_COOKIE_USERNAME = ErrorInfo(4016, "Invalid cookie username", status.HTTP_401_UNAUTHORIZED)
    INVALID_COOKIE_TOKEN = ErrorInfo(4017, "Invalid cookie token", status.HTTP_401_UNAUTHORIZED)
    USER_REGISTRATION_CLOSED = ErrorInfo(4018, "User registration is closed", status.HTTP_403_FORBIDDEN)

    WORD_SET_NOT_FOUND = ErrorInfo(4500, "Word set not found", status.HTTP_404_NOT_FOUND)


