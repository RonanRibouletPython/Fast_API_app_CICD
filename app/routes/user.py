import fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.schemas.user import UserCreate, UserBase
from app.utils.user import create_user, get_user, update_user, get_user_by_name_and_dob, delete_user_by_name_and_dob
from app.db.models.user import User as UserModel
from app.schemas.user import User as UserSchema, UserDelete
from app.utils.logger import logger

users = [
    
]

router = APIRouter()

# @router.get("/users", response_model=List[DateIdeas])
# async def get_posts():
#     return users

@router.post("/users/create", response_model=UserSchema)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the system.

    - If the user does not already exist in the system, create the user and return the newly created user object.
    - If the user already exists in the system, return a 400 status with a message indicating that the user already exists.
    """
    logger.info(f"Attempting to create user: {user}")
    if get_user_by_name_and_dob(db=db, name=user.name, date_of_birth=user.date_of_birth):
        logger.info(f"User {user.name} already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    created_user = create_user(db=db, user=user)
    return created_user	

@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):

    """
    Get a user by their ID.

    - If the user exists, return the user object.
    - If the user does not exist, return a 404 status with a message indicating that the user was not found.
    """
    logger.info(f"Attempting to get user: {user_id}")
    user = get_user(db=db, user_id=user_id)
    if not user:
        logger.info(f"User {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@router.delete("/users/delete")
async def delete_user(user: UserDelete, db: Session = Depends(get_db)):
    """
    Delete a user with their name and date of birth.

    - If the user exists, they are deleted from the system.
    - If the user does not exist, return a 204 status to indicate that the user was not found.
    """
    
    # Log the incoming request
    logger.info(f"Attempting to delete user: {user.name}, DOB: {user.date_of_birth}")
    
    # Validate input data
    if not user.name or not user.date_of_birth:
        logger.warning(f"Invalid input: Missing name or date_of_birth.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both name and date of birth must be provided.",
        )

    try:
        # Attempt to find the user in the database
        existing_user = get_user_by_name_and_dob(db=db, name=user.name, date_of_birth=user.date_of_birth)

        # If user is not found, return 204 No Content
        if not existing_user:
            logger.info(f"User {user.name} with DOB {user.date_of_birth} not found.")
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="User not found.",
            )

        # Proceed with deletion
        delete_user_by_name_and_dob(db=db, name=user.name, date_of_birth=user.date_of_birth)
        db.commit()  # Commit the transaction
        logger.info(f"User {user.name} with DOB {user.date_of_birth} deleted successfully.")

    except Exception as e:
        # Log and handle unexpected exceptions
        logger.error(f"Error occurred while deleting user: {e}")
        db.rollback()  # Roll back in case of any exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred. Please try again later.",
        )
    
@router.put("/users/modify/{user_id}", response_model=UserSchema)
async def update_user_by_id(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    """Update a user by their ID."""
    """Update a user by their name and date of birth."""
    logger.info(f"Attempting to update user: {user.name}, DOB: {user.date_of_birth}")
    updated_user = update_user(db=db, user_id=user_id, user=user)
    
    if not updated_user:
        logger.info(f"User {user.name} with DOB {user.date_of_birth} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return updated_user
    


