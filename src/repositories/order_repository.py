from datetime import datetime

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from src.models.order import Customer, Order, OrderItem, OrderStatus, Product, Supplier


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

    def query(
        self,
        page: int = 1,
        limit: int = 20,
        customer_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        status: OrderStatus | None = None,
        sort: str | None = None,
    ) -> tuple[list[Order], int]:
        q = self._with_relations()
        if customer_id is not None:
            q = q.filter(Order.customer_id == customer_id)
        if date_from is not None:
            q = q.filter(Order.order_date >= date_from)
        if date_to is not None:
            q = q.filter(Order.order_date <= date_to)
        if status is not None:
            q = q.filter(Order.status == status)

        if sort:
            field, _, direction = sort.partition(":")
            column = {
                "orderDate": Order.order_date,
                "orderNumber": Order.order_number,
                "totalAmount": Order.total_amount,
                "id": Order.id,
            }.get(field, Order.id)
            q = q.order_by(desc(column) if direction == "desc" else asc(column))
        else:
            q = q.order_by(Order.id.asc())

        total = q.count()
        items = q.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def update(self, order: Order, data: dict) -> Order:
        for key, value in data.items():
            setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def replace_items(self, order: Order, items: list[OrderItem]) -> None:
        order.items.clear()
        self.db.flush()
        for it in items:
            order.items.append(it)
        self.db.flush()

    def add_item(self, item: OrderItem) -> OrderItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_item(self, order_id: int, item_id: int) -> OrderItem | None:
        return (
            self.db.query(OrderItem)
            .options(joinedload(OrderItem.product).joinedload(Product.supplier))
            .filter(OrderItem.order_id == order_id, OrderItem.id == item_id)
            .first()
        )

    def list_items(self, order_id: int) -> list[OrderItem]:
        return (
            self.db.query(OrderItem)
            .options(joinedload(OrderItem.product).joinedload(Product.supplier))
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    def delete_item(self, item: OrderItem) -> None:
        self.db.delete(item)
        self.db.commit()

    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def query(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        city: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:
        q = self.db.query(Customer)
        if country:
            q = q.filter(Customer.country == country)
        if city:
            q = q.filter(Customer.city == city)
        if search:
            like = f"%{search}%"
            q = q.filter(
                or_(
                    Customer.first_name.ilike(like),
                    Customer.last_name.ilike(like),
                    Customer.phone.ilike(like),
                )
            )
        q = q.order_by(Customer.id.asc())
        total = q.count()
        items = q.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def list_orders(self, customer_id: int) -> list[Order]:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items)
                .joinedload(OrderItem.product)
                .joinedload(Product.supplier),
            )
            .filter(Order.customer_id == customer_id)
            .order_by(Order.id.asc())
            .all()
        )

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update(self, customer: Customer, data: dict) -> Customer:
        for key, value in data.items():
            setattr(customer, key, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def _with_supplier(self):
        return self.db.query(Product).options(joinedload(Product.supplier))

    def get_by_id(self, product_id: int) -> Product | None:
        return self._with_supplier().filter(Product.id == product_id).first()

    def query(
        self,
        page: int = 1,
        limit: int = 20,
        supplier_id: int | None = None,
        search: str | None = None,
        discontinued: bool | None = None,
    ) -> tuple[list[Product], int]:
        q = self._with_supplier()
        if supplier_id is not None:
            q = q.filter(Product.supplier_id == supplier_id)
        if discontinued is not None:
            q = q.filter(Product.is_discontinued == discontinued)
        if search:
            q = q.filter(Product.product_name.ilike(f"%{search}%"))
        q = q.order_by(Product.id.asc())
        total = q.count()
        items = q.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def has_dependencies(self, product_id: int) -> bool:
        return (
            self.db.query(OrderItem)
            .filter(OrderItem.product_id == product_id)
            .first()
            is not None
        )

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, supplier_id: int) -> Supplier | None:
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def query(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Supplier], int]:
        q = self.db.query(Supplier)
        if country:
            q = q.filter(Supplier.country == country)
        if search:
            like = f"%{search}%"
            q = q.filter(
                or_(
                    Supplier.company_name.ilike(like),
                    Supplier.contact_name.ilike(like),
                )
            )
        q = q.order_by(Supplier.id.asc())
        total = q.count()
        items = q.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def list_products(self, supplier_id: int) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.supplier))
            .filter(Product.supplier_id == supplier_id)
            .order_by(Product.id.asc())
            .all()
        )

    def create(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def update(self, supplier: Supplier, data: dict) -> Supplier:
        for key, value in data.items():
            setattr(supplier, key, value)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier
