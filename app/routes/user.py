from app.schemas.activity import DateIdeas
import fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.schemas.user import UserCreate, UserBase
from app.utils.user import create_user, get_user, delete_user, update_user
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

@router.delete("/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by their ID."""
    delete_user(db=db, user_id=user_id)
    
@router.put("/{user_id}", response_model=UserSchema)
async def update_user_by_id(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    """Update a user by their ID."""
    updated_user = update_user(db=db, user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user
    


