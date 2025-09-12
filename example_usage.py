# Ví dụ sử dụng AppException với tự động lấy thông tin file và function

from src.exception.app_exception import AppException, exception_context
from src.exception.error_code import ErrorCode

def example_function_1():
    """Sử dụng cách 1: Tự động trong constructor"""
    print("=== Cách 1: Tự động trong constructor ===")
    try:
        raise AppException(ErrorCode.USER_EXISTED)
    except AppException as e:
        print(f"Error Path: {e.error_path}")
        print(f"Error Code: {e.error_code}")
        print(f"Message: {e.return_message}")

def example_function_2():
    """Sử dụng cách 2: Class method create()"""
    print("\n=== Cách 2: Class method create() ===")
    try:
        raise AppException.create(ErrorCode.USER_EXISTED, alt_message="Custom message")
    except AppException as e:
        print(f"Error Path: {e.error_path}")
        print(f"Error Code: {e.error_code}")
        print(f"Message: {e.return_message}")

@exception_context
def example_function_3():
    """Sử dụng cách 3: Decorator exception_context"""
    print("\n=== Cách 3: Decorator @exception_context ===")
    # Giả lập một exception khác
    raise ValueError("This is a regular Python exception")

def main():
    # Test cách 1
    example_function_1()
    
    # Test cách 2  
    example_function_2()
    
    # Test cách 3
    try:
        example_function_3()
    except AppException as e:
        print(f"Error Path: {e.error_path}")
        print(f"Original exception converted to AppException")
        print(f"Message: {e.return_message}")

if __name__ == "__main__":
    main()
