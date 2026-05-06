from __future__ import annotations
from typing import List, Tuple
from src.core.exceptions import NotFoundError
from src.models.order import Customer, Order
from src.repositories.order_repository import CustomerRepository
from src.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    def list(self, page, limit, country, city, search) -> Tuple[List[Customer], int]:
        return self.repo.list(page=page, limit=limit, country=country, city=city, search=search)

    def get(self, customer_id: int) -> Customer:
        c = self.repo.get(customer_id)
        if c is None:
            raise NotFoundError(f"Cliente {customer_id} no existe")
        return c

    def list_orders(self, customer_id: int) -> List[Order]:
        self.get(customer_id)
        return self.repo.list_orders(customer_id)

    def create(self, payload: CustomerCreate) -> Customer:
        return self.repo.create(Customer(id=0, **payload.model_dump()))

    def update(self, customer_id: int, payload: CustomerUpdate) -> Customer:
        customer = self.get(customer_id)
        return self.repo.update(customer, payload.model_dump(exclude_unset=True))

    def delete(self, customer_id: int) -> None:
        customer = self.get(customer_id)
        self.repo.delete(customer)
