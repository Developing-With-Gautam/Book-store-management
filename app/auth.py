from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from models import User
from sqlalchemy.orm import Session
from database import get_db

JWT_SECRET = "12343dfersdmfgnwrejmdferedrfd"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_TIME = 30

pwd_context = CryptContext(schemes=["sha512_crypt"], deprecated="auto")

oauth2scheme = OAuth2PasswordBearer("auth/login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_jwt_token(data:dict):
    to_encode = data.copy()
    expiryTime = datetime.utcnow()+timedelta(minutes=JWT_EXPIRE_TIME)
    to_encode.update({"exp":expiryTime})

    return jwt.encode(to_encode,JWT_SECRET,algorithm=JWT_ALGORITHM)



oauth2_scheme = OAuth2PasswordBearer('/auth/login')

def verify_user(token :str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token , JWT_SECRET,algorithms=JWT_ALGORITHM)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token not valid")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token not valid")
    
    user = db.query(User).filter( User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    return user

