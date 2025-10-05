from fastapi import APIRouter,Depends,HTTPException,status
from database import get_db
from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate

router = APIRouter(tags=["Books"])

@router.get('/books')
def get_all_books(skip:int=0,limit:int=10,db:Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books


@router.get('/books/{id}')
def get_book_by_id(id:int,db:Session = Depends(get_db)):

    isvalid = db.query(Book).filter(Book.id ==id).first()

    if not isvalid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"book not found with this {id}, Please enter valid id")
    
    return isvalid

@router.post('/books',status_code=status.HTTP_201_CREATED)
def add_new_book(data:BookCreate,db:Session = Depends(get_db)):
    books = Book(title = data.title ,author = data.author ,price = data.price , stock = data.stock)
    db.add(books)
    db.commit()
    db.refresh(books)
    return books

@router.put('/books/{id}')
def update_book(id:int,data:BookCreate,db:Session = Depends(get_db)):

    validid = db.query(Book).filter(Book.id == id).first()
    if not validid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found of particular id")
    
    for key, value in data.dict().items():
        setattr(validid, key, value)
    db.commit()
    db.refresh(validid)
    return validid

@router.delete("/books/{id}")

def delete_book(id:int ,db:Session= Depends(get_db)):
     
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found of particular id")
    
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}


    


    







