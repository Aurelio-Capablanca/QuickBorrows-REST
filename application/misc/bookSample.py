# models/bookmodel.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from application.database.session import SessionLocal

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)



def create_book(db : Session ,title: str, author: str):
    new_book = Book(title=title, author=author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def update_book(db: Session, book_id: int, title: str = None, author: str = None):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    if title:
        book.title = title
    if author:
        book.author = author
    db.commit()
    db.refresh(book)
    return book

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False