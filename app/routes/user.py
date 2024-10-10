from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.schemas.user import UserCreate
from app.utils.user import (
    create_user,
    get_user,
    update_user,
    get_user_by_name,
    delete_user_with_id,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.db.models.user import User as UserModel
from app.schemas.user import User as UserSchema, UserModify
from app.utils.logger import logger
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
except ValueError:
    logger.error("ACCESS_TOKEN_EXPIRE_MINUTES must be a valid integer.")
    raise

router = APIRouter()

@router.post("/user/create/", response_model=UserSchema)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the system.
    """
    logger.info(f"Attempting to create user: {user}")
    existing_user = get_user_by_name(db=db, name=user.name)
    
    if existing_user:
        logger.warning(f"User {user.name} already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    
    created_user = create_user(db=db, user=user)
    logger.info(f"User {created_user.name} created successfully with ID {created_user.id}.")
    return created_user	

@router.get("/user/{user_id}/", response_model=UserSchema)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get user information by their ID.
    """
    logger.info(f"Attempting to get user: {user_id}")
    user = get_user(db=db, user_id=user_id)
    
    if not user:
        logger.info(f"User {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    logger.info(f"User {user_id} retrieved successfully.")
    return user

@router.put("/user/{user_id}", response_model=UserSchema)
async def update_user_by_id(
    user_id: int, 
    user: UserModify, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # Inject the current user
):
    """
    Update a user by their ID.
    """
    logger.info(f"Current user ID: {current_user.id}, attempting to update user with ID: {user_id}")
    
    # Check if the current user matches the user being updated
    if current_user.id != user_id:
        logger.warning(f"User ID {current_user.id} is not authorized to update user ID {user_id}.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to update this user."
        )
    
    updated_user = update_user(db=db, user_id=user_id, user=user)
    
    if not updated_user:
        logger.info(f"User with ID {user_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    db.commit()  # Commit transaction after successful update
    logger.info(f"User with ID {user_id} updated successfully.")
    return updated_user

@router.delete("/user/{user_id}/")
async def delete_user_by_id(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # Inject the current user
):
    """
    Delete a user by their ID.
    """
    logger.info(f"Current user ID: {current_user.id}, attempting to delete user: {user_id}")
    
    # Check if the current user matches the user being deleted
    if current_user.id != user_id:
        logger.warning(f"User ID {current_user.id} is not authorized to delete user ID {user_id}.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to delete this user."
        )

    try:
        delete_user_with_id(db=db, user_id=user_id)
        db.commit()  # Commit the transaction
        logger.info(f"User {user_id} deleted successfully.")
    except Exception as e:
        logger.error(f"Error occurred while deleting user {user_id}: {e}")
        db.rollback()  # Roll back in case of any exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred. Please try again later.",
        )
    
@router.post("/login/")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user and return a JWT token if the credentials are valid.
    """
    logger.info(f"Attempting to log in user: {form_data.username}")
    
    # Get the user from the database using the username from the form data
    user = db.query(UserModel).filter(UserModel.name == form_data.username).first()

    # Verify user existence and password correctness
    if not user or not verify_password(form_data.password, user.password):
        logger.warning(f"Login failed for user: {form_data.username}. Incorrect credentials.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    logger.info(f"User {form_data.username} logged in successfully. Access token generated.")
    
    # Return the token and token type
    return {"access_token": access_token, "token_type": "bearer"}
