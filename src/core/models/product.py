from .base import Base
from sqlalchemy import Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    sale_id: Mapped[int] = mapped_column(Integer, ForeignKey('sales.id'), nullable=True)
