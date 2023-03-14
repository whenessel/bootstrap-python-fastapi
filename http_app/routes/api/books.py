from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_versionizer import api_version
from pydantic import BaseModel

from domains.books.boundary_interfaces import BookServiceInterface
from domains.books.dto import BookData, Book

router = APIRouter(prefix="/books")


class CreateBookResponse(BaseModel):
    book: Book

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
                "book_id": 123,
            }
        }


class CreateBookRequest(BaseModel):
    title: str
    author_name: str

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
            }
        }


"""
The views defined here have the functionalities of two components:

- Controller: transforms data coming from the HTTP Request into
              the data model required to use the application logic

- Presenter:  transforms the data coming from the application logic
              into the format needed for the proper HTTP Response
"""


@api_version(1)
@router.post("/")
@inject
async def create_book(
    data: CreateBookRequest,
    book_service: BookServiceInterface = Depends(
        Provide[BookServiceInterface.__name__]
    ),
) -> CreateBookResponse:
    created_book = await book_service.create_book(book=BookData(**data.dict()))
    return CreateBookResponse(book=created_book)


# Example v2 API with added parameter
@api_version(2)
@router.post("/")
@inject
async def create_book_v2(
    data: CreateBookRequest,
    some_optional_query_param: bool = False,
    book_service: BookServiceInterface = Depends(
        Provide[BookServiceInterface.__name__]
    ),
) -> CreateBookResponse:
    created_book = await book_service.create_book(book=BookData(**data.dict()))
    return CreateBookResponse(book=created_book)
