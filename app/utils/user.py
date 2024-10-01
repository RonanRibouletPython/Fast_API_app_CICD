from sqlalchemy.orm import Session
from app.db.models.user import User as UserModel  # Import the SQLAlchemy model 
from app.schemas.user import User, UserBase, UserCreate, UserDelete, UserModify
from datetime import datetime, date
import sqlalchemy as sa
from app.utils.logger import logger
from typing import Optional


def get_user(db: Session, user_id: int):
    """Get a user by their ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_partner_id(db: Session, partner_id: int):
    """Get a user by their partner's ID."""
    return db.query(UserModel).filter(UserModel.partner_id == partner_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination."""
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate): 
    """Create a new unique user"""
    db_user = UserModel(**user.model_dump())
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

def get_user_by_name_and_dob(db: Session, name: str, date_of_birth: date):
    return db.query(UserModel).filter(UserModel.name == name, UserModel.date_of_birth == date_of_birth).first()

def delete_user_by_name_and_dob(db: Session, name: str, date_of_birth: date):
    user_to_delete = get_user_by_name_and_dob(db, name=name, date_of_birth=date_of_birth)
    if user_to_delete:
        db.delete(user_to_delete)