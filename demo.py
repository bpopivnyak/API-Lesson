from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "sqlite:///./test1.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session() -> Session:
    return SessionLocal()

def create_user(name: str):
    db = get_session()
    book = Book(name=name)
    db.add(book)
    db.commit()
    db.refresh(book)
    db.close()

def list_users():
    db = get_session()
    books = db.query(Book).all()
    db.close()
    print("Всі книжки:")
    for book in books:
        print(f"{book.id}: {book.name}")

def find_user(name: str):
    db = get_session()
    book = db.query(Book).filter(Book.name == name).first()
    db.close()
    if book:
        print(f"Знайшли: {book.id} - {book.name}")
    else:
        print("Книжку ми не змогли знайти, можливо символи були введені неправильно?")

def update_books(book_id: int, new_bookname: str):
    db = get_session()
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.name = new_bookname
        db.commit()
        print(f"Оновлено: ID {book_id} → {new_bookname}")
    else:
        print("Книгу не оновлено, тому що не змогли знайти")
    db.close()

def delete_book(book_id: int):
    db = get_session()
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        print(f"Видалено користувача з ID {book_id}")
    else:
        print("Книжку не видалено, бо не знайшли із-за неправильних введених символів")
    db.close()

if __name__ == "__main__":
    delete_book(2)

