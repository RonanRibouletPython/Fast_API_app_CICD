from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=datetime, nullable=False)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime, nullable=False)