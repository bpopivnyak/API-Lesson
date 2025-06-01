import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, security
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette import status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from pydantic import BaseModel

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
security = HTTPBasic()
class UserLogin(BaseModel):
    username: str
    password: str

def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
@app.delete("/secure-endpoint/")
def secure_endpoint(username=Depends(check_credentials)):
    return {"message": f"Hello, {username}! You are authorized."}


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

    