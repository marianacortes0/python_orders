from src.core.exceptions import NotFoundError
from src.models.order import Product, Supplier
from src.repositories.order_repository import SupplierRepository
from src.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    def __init__(self):
        self.repo = SupplierRepository()

    def list(self, page, limit, country, search) -> tuple[list[Supplier], int]:
        return self.repo.list(page=page, limit=limit, country=country, search=search)

    def get(self, supplier_id: int) -> Supplier:
        s = self.repo.get(supplier_id)
        if s is None:
            raise NotFoundError(f"Proveedor {supplier_id} no existe")
        return s

    def list_products(self, supplier_id: int) -> list[Product]:
        self.get(supplier_id)
        return self.repo.list_products(supplier_id)

    def create(self, payload: SupplierCreate) -> Supplier:
        return self.repo.create(Supplier(id=0, **payload.model_dump()))

    def update(self, supplier_id: int, payload: SupplierUpdate) -> Supplier:
        supplier = self.get(supplier_id)
        return self.repo.update(supplier, payload.model_dump(exclude_unset=True))

    def delete(self, supplier_id: int) -> None:
        supplier = self.get(supplier_id)
        self.repo.delete(supplier)
