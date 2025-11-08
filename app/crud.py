from sqlmodel import Session, select
from .models import Customer, CustomerCreate, CustomerUpdate
from typing import List, Optional

def create_customer(session: Session, customer_data: CustomerCreate) -> Customer:
    customer = Customer.from_orm(customer_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def get_customers(session: Session) -> List[Customer]:
    return session.exec(select(Customer)).all()

def get_customer_by_id(session: Session, customer_id: int) -> Optional[Customer]:
    return session.get(Customer, customer_id)

def update_customer(session: Session, customer_id: int, customer_data: CustomerUpdate) -> Optional[Customer]:
    customer = session.get(Customer, customer_id)
    if not customer:
        return None
    data = customer_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def delete_customer(session: Session, customer_id: int) -> bool:
    customer = session.get(Customer, customer_id)
    if not customer:
        return False
    session.delete(customer)
    session.commit()
    return True
