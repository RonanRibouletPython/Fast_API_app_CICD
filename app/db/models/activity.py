from app.db.db_setup import Base
from app.db.models.mixins import TimestampMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

class Activity(TimestampMixin, Base):
    __tablename__ = "activities"
    __table_args__ = {"schema": "app_schema"}

    id = Column(Integer, primary_key=True)
    activity_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)
    budget = Column(String, nullable=False)
    location = Column(String, nullable=True)
    link_info = Column(URLType, nullable=True)
    user_id = Column(Integer, ForeignKey("app_schema.users.id"), nullable=False)
    description = Column(Text, nullable=True)

    # Foreign keys for user and partner
    user_id = Column(Integer, ForeignKey("app_schema.users.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("app_schema.users.id"), nullable=False)

    # Relationships
    created_by = relationship("User", foreign_keys=[user_id], back_populates="activities_created")
    partner = relationship("User", foreign_keys=[partner_id], back_populates="activities_shared")