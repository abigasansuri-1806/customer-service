from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from datetime import datetime
from .database import get_session
from . import crud, models
from utils.kafka_producer import send_event

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=models.Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: models.CustomerCreate, session: Session = Depends(get_session)):
    db_customer = crud.create_customer(session, customer)
    await send_event("customer.created", {"id": db_customer.customer_id, "name": db_customer.name})
    return db_customer

@router.get("/", response_model=List[models.Customer])
def list_customers(session: Session = Depends(get_session)):
    return crud.get_customers(session)

@router.get("/{customer_id}", response_model=models.Customer)
def get_customer(customer_id: int, session: Session = Depends(get_session)):
    db_customer = crud.get_customer_by_id(session, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=models.Customer)
async def update_customer(customer_id: int, customer: models.CustomerUpdate, session: Session = Depends(get_session)):
    updated = crud.update_customer(session, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    await send_event("customer.updated", {"id": updated.customer_id, "name": updated.name})
    return updated

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    deleted = crud.delete_customer(session, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    await send_event("customer.deleted", {"id": customer_id})
    return None
