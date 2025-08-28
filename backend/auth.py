from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

# Would move this to .env for production. Have left here for ease of setup
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
#######################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token=Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user