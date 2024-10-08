from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import sqlalchemy as sa
from app.utils.logger import logger
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt 
import os
import dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.db.models.user import User as UserModel  # Import the SQLAlchemy model 
from app.schemas.user import User, UserCreate, UserModify
from app.utils.utility import get_db

# Load environment variables from a .env file
dotenv.load_dotenv()
# get the secret key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
except ValueError:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a valid integer.")

# Define the OAuth2 password bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_name(db=db, name=username)  # Get the user from the database
    if user is None:
        raise credentials_exception
    return user

def get_user(db: Session, user_id: int):
    """Get a user by their ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    """Get a user by their name."""
    return db.query(UserModel).filter(UserModel.name == name).first()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Helper functions for hashing and verifying passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(db: Session, user: UserCreate): 
    """Create a new unique user"""
    hashed_password = hash_password(user.password)
    db_user = UserModel(name=user.name, date_of_birth=user.date_of_birth, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserModify) -> Optional[User]:
    """Update a user by their name and date of birth."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if db_user is None:
        return None  # User not found, return None

    if user.name is not None:
        db_user.name = user.name
    if user.date_of_birth is not None:
        db_user.date_of_birth = user.date_of_birth
    if user.partner_id is not None:
        db_user.partner_id = user.partner_id
    db_user.updated_at = datetime.now()

    db.commit()  # Commit the changes
    db.refresh(db_user)  # Refresh the instance to get updated values
    return db_user

def delete_user_with_id(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()