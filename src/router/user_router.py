from fastapi import APIRouter, Depends, HTTPException, status, Body
from controller import UserController
from dto import BaseResponse, CreateUserDTO, UserDTO, UpdateUserDTO

class UserRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/users")
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/create-user", self.create_user, methods=["POST"], response_model=BaseResponse[UserDTO],status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/update-password", self.update_user_password, methods=["PATCH"], response_model=BaseResponse[bool], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/delete-user/{username}", self.delete_user, methods=["DELETE"], response_model=BaseResponse[bool], status_code=status.HTTP_200_OK)

    async def create_user(self, user: CreateUserDTO,controller: UserController = Depends()) -> BaseResponse[UserDTO]:
        return BaseResponse(
            message="User created successfully",
            body=await controller.create_user(user)
        )

    async def update_user_password(
        self, 
        username: str=Body(..., embed=True), 
        old_password: str=Body(..., embed=True), 
        new_password: str=Body(..., embed=True), 
        controller: UserController = Depends()
    ) -> BaseResponse[bool]:
        return BaseResponse(
            message="User password updated successfully",
            body=await controller.update_user_password(username, old_password, new_password)
        )
    
    async def delete_user(self, username: str, controller: UserController = Depends()) -> BaseResponse[bool]:
        return BaseResponse(
            message="User deleted successfully",
            body=await controller.delete_user(username)
        )
    
    @classmethod
    def get_router(cls):
        return cls().router