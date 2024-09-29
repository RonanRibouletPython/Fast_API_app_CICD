from app.db.db_setup import Base 
from app.db.models.mixins import TimestampMixin 
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=True) 

    partner = relationship("User", remote_side=[id], post_update=True) 
    activities = relationship("Activity", back_populates="created_by")