from app.db.db_setup import Base 
from app.db.models.mixins import TimestampMixin 
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class PartnerRequest(TimestampMixin, Base):
    __tablename__ = 'partner_requests'
    __table_args__ = {'schema': 'app_schema'}

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey('app_schema.users.id'), nullable=False)
    requested_id = Column(Integer, ForeignKey('app_schema.users.id'), nullable=False)
    status = Column(String(20), nullable=False, default='pending')  # 'pending', 'accepted', 'rejected'
    test = Column(String(255), nullable=True)
    
    requester = relationship("User", foreign_keys=[requester_id])
    requested = relationship("User", foreign_keys=[requested_id])