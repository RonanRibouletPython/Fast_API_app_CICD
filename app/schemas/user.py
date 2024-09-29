from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    age: int
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