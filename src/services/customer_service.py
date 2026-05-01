from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.models.order import Customer, Order
from src.repositories.order_repository import CustomerRepository
from src.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def list_customers(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        city: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:
        return self.repository.query(
            page=page, limit=limit, country=country, city=city, search=search
        )

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Cliente con id {customer_id} no existe")
        return customer

    def list_customer_orders(self, customer_id: int) -> list[Order]:
        self.get_customer(customer_id)
        return self.repository.list_orders(customer_id)

    def create_customer(self, payload: CustomerCreate) -> Customer:
        customer = Customer(**payload.model_dump())
        return self.repository.create(customer)

    def update_customer(self, customer_id: int, payload: CustomerUpdate) -> Customer:
        customer = self.get_customer(customer_id)
        data = payload.model_dump(exclude_unset=True)
        return self.repository.update(customer, data)
