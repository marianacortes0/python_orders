from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.models.order import Product, Supplier
from src.repositories.order_repository import SupplierRepository
from src.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    def __init__(self, db: Session):
        self.repository = SupplierRepository(db)

    def list_suppliers(
        self,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Supplier], int]:
        return self.repository.query(
            page=page, limit=limit, country=country, search=search
        )

    def get_supplier(self, supplier_id: int) -> Supplier:
        supplier = self.repository.get_by_id(supplier_id)
        if supplier is None:
            raise NotFoundError(f"Proveedor con id {supplier_id} no existe")
        return supplier

    def list_supplier_products(self, supplier_id: int) -> list[Product]:
        self.get_supplier(supplier_id)
        return self.repository.list_products(supplier_id)

    def create_supplier(self, payload: SupplierCreate) -> Supplier:
        supplier = Supplier(**payload.model_dump())
        return self.repository.create(supplier)

    def update_supplier(self, supplier_id: int, payload: SupplierUpdate) -> Supplier:
        supplier = self.get_supplier(supplier_id)
        data = payload.model_dump(exclude_unset=True)
        return self.repository.update(supplier, data)
