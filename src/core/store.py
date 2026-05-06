from __future__ import annotations
from typing import Dict
from src.models.order import Customer, Order, OrderItem, Product, Supplier


class InMemoryStore:
    def __init__(self):
        self.suppliers: Dict[int, Supplier] = {}
        self.products: Dict[int, Product] = {}
        self.customers: Dict[int, Customer] = {}
        self.orders: Dict[int, Order] = {}
        self.order_items: Dict[int, OrderItem] = {}

    def next_id(self, col: dict) -> int:
        return max(col.keys(), default=0) + 1


store = InMemoryStore()
