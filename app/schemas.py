
from pydantic import EmailStr,Field,BaseModel

class UserCreate(BaseModel):
    name:str =Field(...,min_length=3,description="Name of the user")
    email:EmailStr =Field(...,"Enter email of the user")
    password:str = Field(...,min_length=3,description="password of the user")


class BookCreate(BaseModel):
    title:str=Field(...,min_length=1,description="tile of the book")
    author:str=Field(...,min_length=1,description="author of the book")
    price:float = Field(...,description="price of the book")
    stock:int = Field(..., description="Number of copies in stock")


class orderCreate(BaseModel):
    user_id:int
    
class OrderItemCreate(BaseModel):
    order_id:int
    book_id:int
    quantity:int = Field(...,gt=0,description="quantity of this book")




