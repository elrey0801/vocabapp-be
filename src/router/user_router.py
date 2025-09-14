from fastapi import APIRouter, Depends, HTTPException, status
from controller import UserController
from dto import BaseResponse, CreateUserDTO, UserDTO

class UserRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/users")
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/create-user", self.create_user, methods=["POST"], response_model=BaseResponse[UserDTO],status_code=status.HTTP_201_CREATED)

    async def create_user(self, user: CreateUserDTO,controller: UserController = Depends()) -> BaseResponse[UserDTO]:
        return BaseResponse(
            message="User created successfully",
            body=await controller.create_user(user)
        )

    @classmethod
    def get_router(cls):
        return cls().router