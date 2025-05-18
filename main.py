import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List


from starlette.requests import Request
from starlette.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")
database: List[dict] = [
    {"id":1, "book_name": "Куджо", "author": "Стівен Кінг", "rating": 4.9},
    {"id":2, "book_name": "Гаррі Поттер і філософський камінь", "author": "Джоан Роулінг", "rating": 4.7},
    {"id":3, "book_name": "451° по фаренгейту", "author": "Рей Бредбері", "rating": 4.6},
]

@app.get("/main_books")
def read_root(request: Request):
    data = {"message": "Hello, World!"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "database": database})
next_id = 1

class BookCreate(BaseModel):
    book_name: str = Field(..., max_length=15, description="BookModel")
    author: str = Field(..., max_length=15, description="Автор")
    rating: str = Field(..., min_length=4, description="Рейтинг")

class Book(BookCreate):
    id : int

@app.post("/Books/", response_model=Book)
async def create_user(book: BookCreate):
    global next_id

    