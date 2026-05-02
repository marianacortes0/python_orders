from src.models.order import Customer, Order, OrderItem, Product, Supplier


class InMemoryStore:
    def __init__(self):
        self.suppliers: dict[int, Supplier] = {}
        self.products: dict[int, Product] = {}
        self.customers: dict[int, Customer] = {}
        self.orders: dict[int, Order] = {}
        self.order_items: dict[int, OrderItem] = {}

    def next_id(self, col: dict) -> int:
        return max(col.keys(), default=0) + 1


store = InMemoryStore()
