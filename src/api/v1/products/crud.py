from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Product, Sale
from datetime import date


# ------------------------------------
# GET
# ------------------------------------

async def get_all_products(
        session: AsyncSession) -> Sequence[Product]:

    stmt = select(Product).order_by(Product.id.desc())
    result = await session.scalars(stmt)

    return result.all()


async def get_product(
        session: AsyncSession,
        product_id: int) -> Product | None:

    return await session.get(Product, product_id)


async def get_products_by_sale_id(
        session: AsyncSession,
        sale_id: int) -> Sequence[Product] | None:

    stmt = select(Product).filter(Product.sale_id == sale_id)
    result = await session.scalars(stmt)

    return result.all()


async def get_products_by_sale_date(
        session: AsyncSession,
        sale_date: date) -> Sequence[Product] | None:

    stmt = select(Sale.id).filter(Sale.date == sale_date)
    sale = await session.scalars(stmt)
    sale_id = sale.first()

    return await get_products_by_sale_id(session, sale_id)


# ------------------------------------
# POST
# ------------------------------------

async def create_product(
        session: AsyncSession,
        product_create: Product) -> Product:

    product = Product(**product_create.model_dump())
    session.add(product)

    await session.commit()
    await session.refresh(product)

    return product


# ------------------------------------
# PATCH
# ------------------------------------

async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: Product) -> Product:

    for name, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    await session.commit()

    return product


# ------------------------------------
# DELETE
# ------------------------------------

async def delete_product(
        session: AsyncSession,
        product: Product) -> None:

    await session.delete(product)
    await session.commit()
