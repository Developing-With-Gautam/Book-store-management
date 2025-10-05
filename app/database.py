from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL =  "postgresql://postgres:password@localhost:5432/bookstores"
engine = create_engine(DATABASE_URL)

localSession = sessionmaker(bind=engine , autoflush= False, autocommit=False)

Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()
