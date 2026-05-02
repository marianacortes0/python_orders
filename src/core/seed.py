import json
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.models.order import Customer, Order, OrderItem, Product, Supplier

SEED_FILE = Path(__file__).resolve().parents[2] / "Orders.json"


def seed_database(path: Path = SEED_FILE) -> None:
    if not path.exists():
        return

    with open(path, "r", encoding="utf-8") as f:
        orders_data = json.load(f)

    db: Session = SessionLocal()
    try:
        if db.query(Order).first():
            return

        suppliers: dict[int, Supplier] = {}
        products: dict[int, Product] = {}
        customers: dict[int, Customer] = {}

        for od in orders_data:
            c = od["customer"]
            if c["id"] not in customers:
                customers[c["id"]] = Customer(
                    id=c["id"],
                    first_name=c["firstName"],
                    last_name=c["lastName"],
                    city=c.get("city"),
                    country=c.get("country"),
                    phone=c.get("phone"),
                )
                db.add(customers[c["id"]])

            for it in od["items"]:
                p = it["product"]
                s = p["supplier"]
                if s["id"] not in suppliers:
                    suppliers[s["id"]] = Supplier(
                        id=s["id"],
                        company_name=s["companyName"],
                        contact_name=s.get("contactName"),
                        contact_title=s.get("contactTitle"),
                        city=s.get("city"),
                        country=s.get("country"),
                        phone=s.get("phone"),
                        fax=s.get("fax"),
                    )
                    db.add(suppliers[s["id"]])
                if p["id"] not in products:
                    products[p["id"]] = Product(
                        id=p["id"],
                        product_name=p["productName"],
                        supplier_id=s["id"],
                        unit_price=p["unitPrice"],
                        package=p.get("package"),
                        is_discontinued=bool(p.get("isDiscontinued", False)),
                    )
                    db.add(products[p["id"]])

        db.flush()

        for od in orders_data:
            order = Order(
                id=od["id"],
                order_number=od["orderNumber"],
                order_date=datetime.fromisoformat(od["orderDate"]),
                total_amount=od["totalAmount"],
                customer_id=od["customer"]["id"],
            )
            for it in od["items"]:
                order.items.append(
                    OrderItem(
                        id=it["id"],
                        product_id=it["product"]["id"],
                        unit_price=it["unitPrice"],
                        quantity=it["quantity"],
                    )
                )
            db.add(order)

        db.commit()
    finally:
        db.close()
