from __future__ import annotations
from typing import List, Tuple
from src.core.exceptions import ConflictError, NotFoundError
from src.models.order import Product
from src.repositories.order_repository import ProductRepository, SupplierRepository
from src.schemas.product import ProductCreate, ProductReplace, ProductUpdate


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
        self.suppliers = SupplierRepository()

    def list(self, page, limit, supplier_id, search, discontinued) -> Tuple[List[Product], int]:
        return self.repo.list(page=page, limit=limit, supplier_id=supplier_id,
                              search=search, discontinued=discontinued)

    def get(self, product_id: int) -> Product:
        p = self.repo.get(product_id)
        if p is None:
            raise NotFoundError(f"Producto {product_id} no existe")
        return p

    def _require_supplier(self, supplier_id: int) -> None:
        if not self.suppliers.get(supplier_id):
            raise NotFoundError(f"Proveedor {supplier_id} no existe")

    def create(self, payload: ProductCreate) -> Product:
        self._require_supplier(payload.supplier_id)
        return self.repo.create(Product(id=0, **payload.model_dump()))

    def replace(self, product_id: int, payload: ProductReplace) -> Product:
        product = self.get(product_id)
        self._require_supplier(payload.supplier_id)
        return self.repo.update(product, payload.model_dump())

    def update(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get(product_id)
        data = payload.model_dump(exclude_unset=True)
        if "supplier_id" in data:
            self._require_supplier(data["supplier_id"])
        return self.repo.update(product, data)

    def delete(self, product_id: int) -> None:
        product = self.get(product_id)
        if self.repo.has_orders(product_id):
            if product.is_discontinued:
                raise ConflictError("El producto ya está descontinuado y tiene órdenes asociadas")
            self.repo.update(product, {"is_discontinued": True})
            raise ConflictError("El producto tiene órdenes asociadas; se marcó como descontinuado")
        self.repo.delete(product)
