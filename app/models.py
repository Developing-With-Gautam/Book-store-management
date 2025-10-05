from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime,func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id =Column(Integer,autoincrement=True,index=True,primary_key=True)
    name = Column(String,nullable=False)
    email =Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String, default="user")

    orders = relationship("Order",back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer,autoincrement=True,index=True,primary_key=True)
    title =Column(String,nullable=False)
    author = Column(String,nullable=False)
    price =Column(Float,nullable=False)
    stock = Column(Integer,nullable=False ,default=0)
    items = relationship("OrderItem", back_populates="book")

class Order(Base):
    __tablename__ ="orders"
    id = Column(Integer,autoincrement=True,index=True,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime,server_default=func.now())

    user = relationship("User",back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer,autoincrement=True,index=True,primary_key=True)
    order_id = Column(Integer,ForeignKey("orders.id"))
    book_id =  Column(Integer,ForeignKey("books.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    book = relationship("Book", back_populates="items")




    






