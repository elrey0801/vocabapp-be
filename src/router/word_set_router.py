# router/word_set_router.py

from fastapi import APIRouter, Depends, Body
from controller import WordSetController
from dto import BaseResponse, WordSetDTO, UpdateWordSetDTO
from middleware import VerifyCookies
from model import User

class WordSetRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/wordsets")
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/create-wordset", self.create_word_set, methods=["POST"], dependencies=[Depends(VerifyCookies())], response_model=BaseResponse[WordSetDTO], status_code=201)
        self.router.add_api_route("/update-wordset", self.update_word_set, methods=["PATCH"], response_model=BaseResponse[WordSetDTO], status_code=200)
        self.router.add_api_route("/user", self.get_all_word_sets_by_user, methods=["GET"], response_model=BaseResponse[list[WordSetDTO]], status_code=200)
        self.router.add_api_route("/delete-wordset/{word_set_id}", self.delete_word_set, methods=["DELETE"], response_model=BaseResponse[bool], status_code=200)
        
    async def create_word_set(self, name: str=Body(..., embed=True), description: str=Body(None, embed=True), controller: WordSetController = Depends()) -> BaseResponse[WordSetDTO]:
        return BaseResponse(
            message="Word set created successfully",
            body=await controller.create_word_set(name, description)
        )
    
    async def update_word_set(self, update_word_set: UpdateWordSetDTO, controller: WordSetController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[WordSetDTO]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word set updated successfully",
            body=await controller.update_word_set(update_word_set, user.id)
        )

    async def get_all_word_sets_by_user(self, controller: WordSetController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[list[WordSetDTO]]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word sets retrieved successfully",
            body=await controller.get_all_word_sets_by_user(user.id)
        )

    async def delete_word_set(self, word_set_id: int, controller: WordSetController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[bool]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word set deleted successfully",
            body=await controller.delete_word_set(word_set_id, user.id)
        )

    @classmethod
    def get_router(cls):
        return cls().router
