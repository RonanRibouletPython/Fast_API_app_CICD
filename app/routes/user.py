from app.schemas.activity import DateIdeas
import fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.schemas.user import UserCreate, UserBase
from app.utils.user import create_user, get_user
from app.db.models.user import User as UserModel
from app.schemas.user import User as UserSchema

users = [
    
]

router = fastapi.APIRouter()

# @router.get("/users", response_model=List[DateIdeas])
# async def get_posts():
#     return users

@router.post("/users", response_model=UserSchema)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db=db, user=user)
    return created_user	

@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a user by their ID."""
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


