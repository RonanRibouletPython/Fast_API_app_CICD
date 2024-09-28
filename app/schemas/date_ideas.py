from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ActivityType(Enum):
    ARTISTIC = "artistic"
    CULTURAL = "cultural"
    FOOD = "food"
    LEISURE = "leisure"

class Budget(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DateIdeas(BaseModel):
    activity_name: str
    activity_type: ActivityType
    budget: Budget
    location: Optional[str] = None 