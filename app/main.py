from fastapi import FastAPI

app = FastAPI()

@app.get('/')

def homepage():
    return " This is homepage of book store"