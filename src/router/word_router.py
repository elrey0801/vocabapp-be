from fastapi import APIRouter, Depends, Body
from controller import WordController
from dto import BaseResponse, WordDTO, UpdateWordDTO, CreateWordDTO
from middleware import VerifyCookies
from model import User

class WordRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/wordsets")
        self.setup_routes()
    
    def setup_routes(self):
        self.router.add_api_route("/create-word", self.create_word, methods=["POST"], response_model=BaseResponse[WordDTO], status_code=201)
        self.router.add_api_route("/update-word", self.update_word, methods=["PATCH"], response_model=BaseResponse[WordDTO], status_code=200)
        self.router.add_api_route("/words-by-wordset/{word_set_id}", self.get_all_words_by_word_set, methods=["POST"], response_model=BaseResponse[list[WordDTO]], status_code=200)
        self.router.add_api_route("/delete-word/{word_id}", self.delete_word, methods=["DELETE"], response_model=BaseResponse[bool], status_code=200)
    
    async def create_word(self, word: CreateWordDTO, controller: WordController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[WordDTO]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word created successfully",
            body=await controller.create_word(word, user.id)
        )
    
    async def update_word(self, update_word: UpdateWordDTO, controller: WordController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[WordDTO]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word updated successfully",
            body=await controller.update_word(update_word, user.id)
        )
    
    async def get_all_words_by_word_set(self, word_set_id: int, controller: WordController = Depends(), auth_info: dict = Depends(VerifyCookies())
    ) -> BaseResponse[list[WordDTO]]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Words fetched successfully",
            body=await controller.get_all_words_by_word_set(word_set_id, user.id)
        )
    
    async def delete_word(self, word_id: int, controller: WordController = Depends(), auth_info: dict = Depends(VerifyCookies())) -> BaseResponse[bool]:
        user: User = auth_info.get("user")
        return BaseResponse(
            message="Word deleted successfully",
            body=await controller.delete_word(word_id, user.id)
        )
        
    @classmethod
    def get_router(cls):
        return cls().router