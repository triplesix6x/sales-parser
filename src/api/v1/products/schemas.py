from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: Decimal
    category: str
    sale_id: int


class ProductCreate(ProductBase):
    pass


class ProductDelete(ProductBase):
    pass


class ProductRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True)
    id: int


class ProductUpdate(ProductBase):
    name: str | None = None
    quantity: int | None = None
    price: Decimal | None = None
    category: str | None = None
    sale_id: int | None = None
