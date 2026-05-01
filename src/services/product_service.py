from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.models.order import Product
from src.repositories.order_repository import ProductRepository, SupplierRepository
from src.schemas.product import ProductCreate, ProductReplace, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.suppliers = SupplierRepository(db)

    def list_products(
        self,
        page: int = 1,
        limit: int = 20,
        supplier_id: int | None = None,
        search: str | None = None,
        discontinued: bool | None = None,
    ) -> tuple[list[Product], int]:
        return self.repository.query(
            page=page,
            limit=limit,
            supplier_id=supplier_id,
            search=search,
            discontinued=discontinued,
        )

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Producto con id {product_id} no existe")
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        if not self.suppliers.get_by_id(payload.supplier_id):
            raise NotFoundError(f"Proveedor con id {payload.supplier_id} no existe")
        product = Product(**payload.model_dump())
        return self.repository.create(product)

    def replace_product(self, product_id: int, payload: ProductReplace) -> Product:
        product = self.get_product(product_id)
        if not self.suppliers.get_by_id(payload.supplier_id):
            raise NotFoundError(f"Proveedor con id {payload.supplier_id} no existe")
        return self.repository.update(product, payload.model_dump())

    def update_product(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        data = payload.model_dump(exclude_unset=True)
        if "supplier_id" in data and not self.suppliers.get_by_id(data["supplier_id"]):
            raise NotFoundError(f"Proveedor con id {data['supplier_id']} no existe")
        return self.repository.update(product, data)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        if self.repository.has_dependencies(product_id):
            if product.is_discontinued:
                raise ConflictError(
                    "El producto tiene órdenes asociadas y ya está descontinuado"
                )
            self.repository.update(product, {"is_discontinued": True})
            raise ConflictError(
                "El producto tiene órdenes asociadas; se marcó como descontinuado"
            )
        self.repository.delete(product)
