from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Product, Sale
from datetime import date
from redis import Redis
from .utils import product_from_dict, product_to_dict
import simplejson


# ------------------------------------
# GET
# ------------------------------------

async def get_all_products(
        session: AsyncSession,
        redis: Redis) -> Sequence[Product]:

    cache_key = "products:all"
    cached_products = redis.get(cache_key)

    if cached_products:
        return [product_from_dict(product) for product in simplejson.loads(cached_products)]

    stmt = select(Product).order_by(Product.id.desc())
    result = await session.scalars(stmt)
    products = result.all()

    if products:
        redis.set(cache_key, simplejson.dumps([product_to_dict(product) for product in products]), ex=600)
    return products


async def get_product(
        session: AsyncSession,
        product_id: int,
        redis: Redis) -> Product | None:

    cache_key = f"products:{product_id}"
    cached_product = redis.get(cache_key)

    if cached_product:
        return product_from_dict(simplejson.loads(cached_product))

    product = await session.get(Product, product_id)

    if product:
        redis.set(cache_key, simplejson.dumps(product_to_dict(product)), ex=600)
    return product


async def get_products_by_sale_id(
        session: AsyncSession,
        sale_id: int,
        redis: Redis) -> Sequence[Product] | None:

    cache_key = f"products:sale_id:{sale_id}"
    cached_products = redis.get(cache_key)

    if cached_products:
        return [product_from_dict(product) for product in simplejson.loads(cached_products)]

    stmt = select(Product).filter(Product.sale_id == sale_id)
    result = await session.scalars(stmt)
    products = result.all()

    if products:
        redis.set(cache_key, simplejson.dumps([product_to_dict(product) for product in products]), ex=600)
    return products


async def get_products_by_sale_date(
        session: AsyncSession,
        sale_date: date,
        redis: Redis) -> Sequence[Product] | None:

    cache_key = f"products:sale_date:{sale_date.isoformat()}"
    cached_products = redis.get(cache_key)

    if cached_products:
        return [product_from_dict(product) for product in simplejson.loads(cached_products)]

    stmt = select(Sale.id).filter(Sale.date == sale_date)
    sale = await session.scalars(stmt)
    sale_id = sale.first()
    products = await get_products_by_sale_id(redis=redis, session=session, sale_id=sale_id)

    if products:
        redis.set(cache_key, simplejson.dumps([product_to_dict(product) for product in products]), ex=600)
    return products

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
