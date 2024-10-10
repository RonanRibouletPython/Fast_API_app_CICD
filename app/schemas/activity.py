from pydantic import BaseModel, HttpUrl, Field
from enum import Enum
from typing import Optional

class ActivityType(str, Enum):
    ARTISTIC = "artistic"
    CULTURAL = "cultural"
    FOOD = "food"
    LEISURE = "leisure"

class Budget(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ActivityCreate(BaseModel):
    activity_name: str
    activity_type: ActivityType
    budget: Budget
    location: Optional[str] = None
    link_info: Optional[HttpUrl] = None
    description: Optional[str] = None
    partner_id: int  # Ensure the activity is linked to a partner

class ActivityResponse(BaseModel):
    id: int
    activity_name: str
    activity_type: ActivityType  # Using enum for consistency
    budget: Budget  # Using enum for consistency
    location: Optional[str] = None
    link_info: Optional[HttpUrl] = None
    description: Optional[str] = None
    user_id: int
    partner_id: int  # Include partner_id in the response

    class Config:
        from_attributes = True  # Allows using ORM models directly
