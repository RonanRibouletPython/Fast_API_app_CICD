from sqlalchemy.orm import Session
from app.db.models.user import User as UserModel  # Import the SQLAlchemy model 
from app.schemas.user import User, UserBase, UserCreate
from datetime import datetime

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
    """Create a new user."""
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user by their ID."""
    db.query(UserModel).filter(UserModel.id == user_id).delete()
    db.commit()

def update_user(db: Session, user_id: int, user: UserBase):
    """Update a user by their ID."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db_user.name = user.name
    db_user.age = user.age
    db_user.partner_id = user.partner_id
    db_user.updated_at = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user