import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
templates = Jinja2Templates(directory="templates")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class BookCreate(BaseModel):
    name: str

@app.post("/books/")
def create_user(book: BookCreate, db: Session = Depends(get_db)):
    db_user = Book(name=book.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/books/")
def read_users(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.get("/books_html/")
def read_users_html(request: Request, db: Session = Depends(get_db)):
    users = db.query(Book).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users,})

uvicorn.run(app)

    