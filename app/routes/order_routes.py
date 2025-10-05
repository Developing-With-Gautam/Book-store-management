from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from schemas import orderCreate
from models import Order,User
from database import get_db
from typing import List
from auth import verify_user


router = APIRouter(
    tags=["Orders"]
    )

@router.post('/orders')
def create_order(data:orderCreate,db:Session= Depends(get_db),create_user:User = Depends(verify_user)):

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    userBook = Order(user_id = data.user_id)
    db.add(userBook)
    db.commit()
    db.refresh(userBook)
    return {"order_id": userBook.id, "user_id": userBook.user_id, "created_at":userBook.created_at}


@router.get("/orders")
def get_orders(db: Session = Depends(get_db),create_user:User = Depends(verify_user)):
    return db.query(Order).all()
    

@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db),create_user:User = Depends(verify_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order.id,
        "user": order.user.name,
        "created_at": order.created_at,
        "items": [
            {
                "book_id": item.book.id,
                "title": item.book.title,
                "author": item.book.author,
                "price": item.book.price,
                "quantity": item.quantity
            }
            for item in order.items
        ]
    }


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db),create_user:User = Depends(verify_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
