from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

from src.core.store import store
from src.models.order import Customer, Order, OrderItem, Product, Supplier

SEED_FILE = Path(__file__).resolve().parents[2] / "Orders.json"


def seed_database(path: Path = SEED_FILE) -> None:
    if not path.exists() or store.orders:
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for od in data:
        c = od["customer"]
        if c["id"] not in store.customers:
            store.customers[c["id"]] = Customer(
                id=c["id"], first_name=c["firstName"], last_name=c["lastName"],
                city=c.get("city"), country=c.get("country"), phone=c.get("phone"),
            )
        for it in od["items"]:
            p, s = it["product"], it["product"]["supplier"]
            if s["id"] not in store.suppliers:
                store.suppliers[s["id"]] = Supplier(
                    id=s["id"], company_name=s["companyName"],
                    contact_name=s.get("contactName"), contact_title=s.get("contactTitle"),
                    city=s.get("city"), country=s.get("country"),
                    phone=s.get("phone"), fax=s.get("fax"),
                )
            if p["id"] not in store.products:
                store.products[p["id"]] = Product(
                    id=p["id"], product_name=p["productName"], supplier_id=s["id"],
                    unit_price=p["unitPrice"], package=p.get("package"),
                    is_discontinued=bool(p.get("isDiscontinued", False)),
                )

    for od in data:
        order = Order(
            id=od["id"], order_number=od["orderNumber"],
            order_date=datetime.fromisoformat(od["orderDate"]),
            total_amount=od["totalAmount"], customer_id=od["customer"]["id"],
        )
        store.orders[order.id] = order
        for it in od["items"]:
            item = OrderItem(
                id=it["id"], order_id=od["id"], product_id=it["product"]["id"],
                unit_price=it["unitPrice"], quantity=it["quantity"],
            )
            store.order_items[item.id] = item
