# exceptions/app_exception.py

import inspect
from pathlib import Path
from exception.error_code import ErrorCode

class AppException(Exception):
    def __init__(self, error_code: ErrorCode, alt_message: str = None, return_message: str = None, error_path: str = None) -> None:
        if alt_message:
            super().__init__(alt_message)
        else:
            super().__init__(error_code.value.message)
        self.error_code = error_code
        
        if error_path is None:
            frame = inspect.currentframe().f_back
            filename = Path(frame.f_code.co_filename).name
            function_name = frame.f_code.co_name
            self.error_path = f"[{filename}]:[{function_name}]"
        else:
            self.error_path = error_path
            
        self.return_message = return_message if return_message else alt_message if alt_message else error_code.value.message