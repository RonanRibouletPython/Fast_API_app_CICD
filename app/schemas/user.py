from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    date_of_birth: date
    partner_id: Optional[int] = None
    
class UserModify(UserBase):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    partner_id: Optional[int] = None

class UserCreate(UserBase):
    ...
    
class UserDelete(BaseModel):
    name: str
    date_of_birth: date
    
class User(UserBase):
    id: int
    # partner_id_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes  = True