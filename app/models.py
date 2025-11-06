from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CustomerBase(SQLModel):
    name: str
    email: str
    phone: str
    kyc_status: str = "PENDING"

class Customer(CustomerBase, table=True):
    customer_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    kyc_status: Optional[str] = None
