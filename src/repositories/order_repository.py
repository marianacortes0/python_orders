from sqlalchemy.orm import Session, joinedload

from src.models.order import Customer, Order, OrderItem, Product, Supplier


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def _with_relations(self):
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items)
                .joinedload(OrderItem.product)
                .joinedload(Product.supplier),
            )
        )

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Order | None:
        return self._with_relations().filter(Order.id == order_id).first()

    def get_by_number(self, order_number: str) -> Order | None:
        return (
            self._with_relations().filter(Order.order_number == order_number).first()
        )

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return self._with_relations().offset(skip).limit(limit).all()

    def update(self, order: Order, data: dict) -> Order:
        for key, value in data.items():
            setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int) -> Product | None:
        return (
            self.db.query(Product)
            .options(joinedload(Product.supplier))
            .filter(Product.id == product_id)
            .first()
        )

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.supplier))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, supplier_id: int) -> Supplier | None:
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Supplier]:
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def create(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier
