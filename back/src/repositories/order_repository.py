from copy import copy
from datetime import datetime

from src.core.store import store
from src.models.order import Customer, Order, OrderItem, OrderStatus, Product, Supplier


def _patch(obj, data: dict):
    for k, v in data.items():
        setattr(obj, k, v)
    return obj


def _page(items: list, page: int, limit: int) -> tuple[list, int]:
    return items[(page - 1) * limit : page * limit], len(items)


class OrderRepository:
    def _build_item(self, item: OrderItem) -> OrderItem:
        it = copy(item)
        if prod := store.products.get(item.product_id):
            p = copy(prod)
            p.supplier = store.suppliers.get(prod.supplier_id)
            it.product = p
        return it

    def _build(self, order: Order) -> Order:
        o = copy(order)
        o.customer = store.customers.get(order.customer_id)
        raw = sorted(
            (i for i in store.order_items.values() if i.order_id == order.id),
            key=lambda x: x.id,
        )
        o.items = [self._build_item(i) for i in raw]
        return o

    def create(self, order: Order) -> Order:
        order.id = store.next_id(store.orders)
        items, order.items, order.customer = order.items[:], [], None
        store.orders[order.id] = order
        for item in items:
            item.id = store.next_id(store.order_items)
            item.order_id = order.id
            store.order_items[item.id] = item
        return self._build(order)

    def get(self, order_id: int) -> Order | None:
        o = store.orders.get(order_id)
        return self._build(o) if o else None

    def get_by_number(self, number: str) -> Order | None:
        for o in store.orders.values():
            if o.order_number == number:
                return self._build(o)
        return None

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        customer_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        status: OrderStatus | None = None,
        sort: str | None = None,
    ) -> tuple[list[Order], int]:
        items = list(store.orders.values())
        if customer_id is not None:
            items = [o for o in items if o.customer_id == customer_id]
        if date_from:
            items = [o for o in items if o.order_date >= date_from]
        if date_to:
            items = [o for o in items if o.order_date <= date_to]
        if status:
            items = [o for o in items if o.status == status]

        field_name, _, direction = (sort or "id:asc").partition(":")
        key = {"orderDate": lambda o: o.order_date, "orderNumber": lambda o: o.order_number,
               "totalAmount": lambda o: o.total_amount}.get(field_name, lambda o: o.id)
        items.sort(key=key, reverse=(direction == "desc"))

        page_items, total = _page(items, page, limit)
        return [self._build(o) for o in page_items], total

    def update(self, order: Order, data: dict) -> Order:
        return self._build(_patch(store.orders[order.id], data))

    def recalculate_total(self, order_id: int) -> None:
        items = [i for i in store.order_items.values() if i.order_id == order_id]
        store.orders[order_id].total_amount = round(sum(i.unit_price * i.quantity for i in items), 2)

    def replace_items(self, order: Order, new_items: list[OrderItem]) -> None:
        for k in [k for k, v in store.order_items.items() if v.order_id == order.id]:
            del store.order_items[k]
        for item in new_items:
            item.id = store.next_id(store.order_items)
            item.order_id = order.id
            store.order_items[item.id] = item

    def add_item(self, item: OrderItem) -> OrderItem:
        item.id = store.next_id(store.order_items)
        store.order_items[item.id] = item
        return item

    def get_item(self, order_id: int, item_id: int) -> OrderItem | None:
        item = store.order_items.get(item_id)
        if not item or item.order_id != order_id:
            return None
        return self._build_item(item)

    def update_item(self, item_id: int, data: dict) -> None:
        if raw := store.order_items.get(item_id):
            _patch(raw, data)

    def list_items(self, order_id: int) -> list[OrderItem]:
        raw = sorted(
            (i for i in store.order_items.values() if i.order_id == order_id),
            key=lambda x: x.id,
        )
        return [self._build_item(i) for i in raw]

    def delete_item(self, item: OrderItem) -> None:
        store.order_items.pop(item.id, None)

    def delete(self, order: Order) -> None:
        for k in [k for k, v in store.order_items.items() if v.order_id == order.id]:
            del store.order_items[k]
        store.orders.pop(order.id, None)


class CustomerRepository:
    def get(self, customer_id: int) -> Customer | None:
        return store.customers.get(customer_id)

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        city: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:
        items = list(store.customers.values())
        if country:
            items = [c for c in items if c.country == country]
        if city:
            items = [c for c in items if c.city == city]
        if search:
            s = search.lower()
            items = [
                c for c in items
                if s in (c.first_name or "").lower()
                or s in (c.last_name or "").lower()
                or s in (c.phone or "").lower()
            ]
        items.sort(key=lambda c: c.id)
        return _page(items, page, limit)

    def list_orders(self, customer_id: int) -> list[Order]:
        repo = OrderRepository()
        orders = sorted(
            (o for o in store.orders.values() if o.customer_id == customer_id),
            key=lambda o: o.id,
        )
        return [repo._build(o) for o in orders]

    def create(self, customer: Customer) -> Customer:
        customer.id = store.next_id(store.customers)
        store.customers[customer.id] = customer
        return customer

    def update(self, customer: Customer, data: dict) -> Customer:
        return _patch(store.customers[customer.id], data)


class ProductRepository:
    def _attach(self, product: Product) -> Product:
        p = copy(product)
        p.supplier = store.suppliers.get(product.supplier_id)
        return p

    def get(self, product_id: int) -> Product | None:
        p = store.products.get(product_id)
        return self._attach(p) if p else None

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        supplier_id: int | None = None,
        search: str | None = None,
        discontinued: bool | None = None,
    ) -> tuple[list[Product], int]:
        items = list(store.products.values())
        if supplier_id is not None:
            items = [p for p in items if p.supplier_id == supplier_id]
        if discontinued is not None:
            items = [p for p in items if p.is_discontinued == discontinued]
        if search:
            s = search.lower()
            items = [p for p in items if s in p.product_name.lower()]
        items.sort(key=lambda p: p.id)
        page_items, total = _page(items, page, limit)
        return [self._attach(p) for p in page_items], total

    def has_orders(self, product_id: int) -> bool:
        return any(i.product_id == product_id for i in store.order_items.values())

    def create(self, product: Product) -> Product:
        product.id = store.next_id(store.products)
        store.products[product.id] = product
        return self._attach(product)

    def update(self, product: Product, data: dict) -> Product:
        return self._attach(_patch(store.products[product.id], data))

    def delete(self, product: Product) -> None:
        store.products.pop(product.id, None)


class SupplierRepository:
    def get(self, supplier_id: int) -> Supplier | None:
        return store.suppliers.get(supplier_id)

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Supplier], int]:
        items = list(store.suppliers.values())
        if country:
            items = [s for s in items if s.country == country]
        if search:
            sl = search.lower()
            items = [
                s for s in items
                if sl in (s.company_name or "").lower()
                or sl in (s.contact_name or "").lower()
            ]
        items.sort(key=lambda s: s.id)
        return _page(items, page, limit)

    def list_products(self, supplier_id: int) -> list[Product]:
        repo = ProductRepository()
        products = sorted(
            (p for p in store.products.values() if p.supplier_id == supplier_id),
            key=lambda p: p.id,
        )
        return [repo._attach(p) for p in products]

    def create(self, supplier: Supplier) -> Supplier:
        supplier.id = store.next_id(store.suppliers)
        store.suppliers[supplier.id] = supplier
        return supplier

    def update(self, supplier: Supplier, data: dict) -> Supplier:
        return _patch(store.suppliers[supplier.id], data)
