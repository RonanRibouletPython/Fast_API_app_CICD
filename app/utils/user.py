from sqlalchemy.orm import Session
from app.db.models.user import User as UserModel  # Import the SQLAlchemy model 
from app.schemas.user import User, UserBase, UserCreate

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