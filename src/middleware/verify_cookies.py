from model import User, Role, TokenType
from controller import AuthController, UserController
from fastapi import Request, Response, Depends
from typing import Any, Dict
from dto import TokenPair, TokenDTO
from exception import AppException, ErrorCode
from config import logger
from util import CookiesUtil

class VerifyCookies:
    def __init__(self, minimum_role: Role = Role.TRIAL_USER):
        self.minimum_role = minimum_role
        self.access_token_id_cookie = "access_token_id"
        self.refresh_token_id_cookie = "refresh_token_id"
        self.access_token_cookie = "access_token"
        self.refresh_token_cookie = "refresh_token"
        self.username_cookie = "username"
    
    async def __call__(
            self,
            request: Request,
            response: Response,
            auth_controller: AuthController = Depends(),
            user_controller: UserController = Depends()
        ) -> Dict[str, Any]:
        
        try:
            access_token = TokenDTO(
                token=request.cookies.get(self.access_token_cookie),
                id=request.cookies.get(self.access_token_id_cookie),
                token_type=TokenType.ACCESS
            )
            refresh_token = TokenDTO(
                token=request.cookies.get(self.refresh_token_cookie),
                id=request.cookies.get(self.refresh_token_id_cookie),
                token_type=TokenType.REFRESH
            )
            username = request.cookies.get(self.username_cookie)
        except:
            raise AppException(
                error_code=ErrorCode.INVALID_COOKIE_TOKEN, 
                alt_message="Missing authentication cookies"
            )
        
        if username is None:
            raise AppException(error_code=ErrorCode.INVALID_COOKIE_USERNAME)
        if access_token.token is None or access_token.id is None:
            raise AppException(error_code=ErrorCode.INVALID_COOKIE_TOKEN)

        user: User = await user_controller.get_user_by_username(username)
        if user is None:
            raise AppException(error_code=ErrorCode.USER_NOT_FOUND)
        if not user.is_active:
            raise AppException(error_code=ErrorCode.INACTIVATED_USER)
        if user.role < self.minimum_role:
            raise AppException(error_code=ErrorCode.PERMISSION_DENIED)
        logger.info(f"User [{user.username}] calls the API [{request.url.path}]")
        
        if not await auth_controller.verify_token(access_token):
            logger.info(f"Access token invalid. Verifying refresh token")
            if not await auth_controller.verify_token(refresh_token):
                raise AppException(error_code=ErrorCode.INVALID_TOKEN, alt_message="Both access and refresh tokens are invalid")
            
            auth_controller.revoke_token(access_token)
            auth_controller.revoke_token(refresh_token)
            token_pair: TokenPair = await auth_controller.create_token_pair(user)
            CookiesUtil.set_auth_cookies(response=response, token_pair=token_pair, username=user.username)
        
        return {
            "username": username,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }
        