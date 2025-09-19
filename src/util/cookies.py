from fastapi import Response
from dto import TokenPair
from config.env_config import settings

class CookiesUtil:
    @staticmethod
    def set_cookies(response: Response, key: str, value: str, max_age: int, httponly: bool = True, secure: bool = True, samesite: str = "none", partitioned: bool = True):
        cookie_str = f"{key}={value}; Max-Age={max_age}; Path=/"
        if httponly:
            cookie_str += "; HttpOnly"
        if settings.PRODUCTION_MODE and secure:
            cookie_str += "; Secure"
        if settings.PRODUCTION_MODE and partitioned:
            cookie_str += "; Partitioned"
        if settings.PRODUCTION_MODE and samesite:
            cookie_str += f"; SameSite={samesite}"

        response.headers.append("Set-Cookie", cookie_str)
    
    @staticmethod
    def delete_cookies(response: Response, key: str):
        cookie_str = f"{key}=; Max-Age=0; Path=/"
        if settings.PRODUCTION_MODE:
            cookie_str += "; Secure; SameSite=none; Partitioned"
        cookie_str += "; HttpOnly"
        
        response.headers.append("Set-Cookie", cookie_str)

    @staticmethod
    def set_auth_cookies(response: Response, token_pair: TokenPair, username: str):
        # Set to max age for all tokens to retain the same expiration time
        CookiesUtil.set_cookies(
            response=response,
            key="access_token",
            value=token_pair.access_token.token,
            max_age=settings.REFRESH_TOKEN_MAX_AGE,
        )
        CookiesUtil.set_cookies(
            response=response,
            key="access_token_id",
            value=str(token_pair.access_token.id),
            max_age=settings.REFRESH_TOKEN_MAX_AGE,
        )
        CookiesUtil.set_cookies(
            response=response,
            key="refresh_token",
            value=token_pair.refresh_token.token,
            max_age=settings.REFRESH_TOKEN_MAX_AGE,
        )
        CookiesUtil.set_cookies(
            response=response,
            key="refresh_token_id",
            value=str(token_pair.refresh_token.id),
            max_age=settings.REFRESH_TOKEN_MAX_AGE,
        )
        CookiesUtil.set_cookies(
            response=response,
            key="username",
            value=username,
            max_age=settings.REFRESH_TOKEN_MAX_AGE,
        )
    
    @staticmethod
    def delete_auth_cookies(response: Response):
        CookiesUtil.delete_cookies(response=response, key="access_token")
        CookiesUtil.delete_cookies(response=response, key="access_token_id")
        CookiesUtil.delete_cookies(response=response, key="refresh_token")
        CookiesUtil.delete_cookies(response=response, key="refresh_token_id")
        CookiesUtil.delete_cookies(response=response, key="username")