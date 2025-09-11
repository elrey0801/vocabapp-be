# exceptions/app_exception.py

from exception.error_code import ErrorCode

class AppException(Exception):
    def __init__(self, error_code: ErrorCode, error_path: str, alt_message: str = None, return_message: str = None) -> None:
        if alt_message:
            super().__init__(alt_message)
        else:
            super().__init__(error_code.value.message)
        self.error_code = error_code
        self.error_path = error_path
        self.return_message = return_message if return_message else alt_message if alt_message else error_code.value.message