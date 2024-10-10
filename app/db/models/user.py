from app.db.db_setup import Base 
from app.db.models.mixins import TimestampMixin 
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.models.activity import Activity

class User(TimestampMixin, Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'app_schema'}

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)  # Ensure it's 255 or another reasonable length
    name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    partner_id = Column(Integer, ForeignKey('app_schema.users.id'), nullable=True)

    # Activities created by this user
    activities_created = relationship("Activity", foreign_keys=[Activity.user_id], back_populates="created_by")

    # Activities shared with the user by their partner
    activities_shared = relationship("Activity", foreign_keys=[Activity.partner_id], back_populates="partner")