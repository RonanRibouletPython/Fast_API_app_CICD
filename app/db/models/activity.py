from app.db.db_setup import Base
from app.db.models.mixins import TimestampMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

class Activity(TimestampMixin, Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    activity_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)
    budget = Column(String, nullable=False)
    location = Column(String, nullable=True)
    link_info = Column(URLType, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)  # New column added!

    created_by = relationship("User", back_populates="activities")