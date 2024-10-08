from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    date_of_birth: date
    password: str
    
class UserModify(UserBase):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    password: Optional[str] = None
    partner_id: Optional[int] = None
    

class UserCreate(UserBase):
    ...
    
class User(UserBase):
    id: int
    # partner_id_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes  = True