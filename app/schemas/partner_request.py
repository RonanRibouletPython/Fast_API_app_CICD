from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PartnerRequestBase(BaseModel):
    requested_id: int
    status: Optional[str] = "pending"

class PartnerRequestCreate(PartnerRequestBase):
    pass

class PartnerRequestUpdate(BaseModel):
    status: Optional[str] = None

class PartnerRequest(BaseModel):
    id: int
    requester_id: int
    requested_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True