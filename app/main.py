from fastapi import FastAPI
from routes import book_routes,order_routes,user_routes
from database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get('/')
def homepage():
    return "This is the homepage of the book store"

app.include_router(book_routes.router)
app.include_router(order_routes.router)
app.include_router(user_routes.router)