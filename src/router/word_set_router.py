# router/word_set_router.py

from fastapi import APIRouter, Depends, Body
from controller import WordSetController
from dto import BaseResponse
from dto import WordSetDTO

class WordSetRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/wordsets")
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/create-wordset", self.create_word_set, methods=["POST"], response_model=BaseResponse[WordSetDTO], status_code=201)
        
    def create_word_set(self, name: str=Body(..., embed=True), description: str=Body(None, embed=True), controller: WordSetController = Depends()) -> BaseResponse[WordSetDTO]:
        return BaseResponse(
            message="Word set created successfully",
            body=controller.create_word_set(name, description)
        )

    @classmethod
    def get_router(cls):
        return cls().router
