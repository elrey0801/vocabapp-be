# routers/auth_routes.py

from fastapi import APIRouter, Response, Request, Depends, Body
from dto import BaseResponse, TokenPair, UserDTO
from controller import UserController, AuthController
from util import CookiesUtil
from middleware import VerifyCookies
from model import User


class AuthRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/auth")
        self.setup_routes()
    
    def setup_routes(self):
        self.router.add_api_route("/login", self.login, methods=["POST"], response_model=BaseResponse[bool], status_code=200)
        self.router.add_api_route("/whoami", self.who_am_i, methods=["GET"], response_model=BaseResponse[UserDTO], status_code=200)
        self.router.add_api_route("/logout", self.logout, methods=["GET"], response_model=BaseResponse[bool], status_code=200)

    
    async def login(
        self, 
        response: Response, 
        username: str=Body(..., embed=True), 
        password: str=Body(..., embed=True), 
        auth_controller: AuthController = Depends()
    ) -> BaseResponse[bool]:
        token_pair: TokenPair = await auth_controller.login(username, password)
        CookiesUtil.set_auth_cookies(
            response=response,
            token_pair=token_pair,
            username=username,
        )
        return BaseResponse(
            message="Login successful",
            body=True
        )
        
    async def logout(
        self, 
        response: Response
    ) -> BaseResponse[bool]:
        CookiesUtil.delete_auth_cookies(response)
        return BaseResponse(
            message="Logout successful",
            body=True
        )    
    
    async def who_am_i(
        self,
        auth_info: dict = Depends(VerifyCookies())
    ) -> BaseResponse[UserDTO]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="User fetched successfully",
            body=UserDTO.model_validate(user)
        )
    
    @classmethod
    def get_router(cls):
        return cls().router