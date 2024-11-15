from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from core.models import Sale
from redis import Redis
from .utils import sale_to_dict, sale_from_dict
import simplejson


# ------------------------------------
# GET
# ------------------------------------

async def get_all_sales(
        session: AsyncSession,
        redis: Redis) -> Sequence[Sale]:

    cache_key = "sales:all"
    cached_sales = redis.get(cache_key)

    if cached_sales:
        return [sale_from_dict(sale) for sale in simplejson.loads(cached_sales)]

    stmt = select(Sale).order_by(Sale.id.desc())
    result = await session.scalars(stmt)
    sales = result.all()

    if sales:
        redis.set(cache_key, simplejson.dumps([sale_to_dict(sale) for sale in sales]), ex=600)
    return sales


async def get_sale(
        session: AsyncSession,
        sale_id: int,
        redis: Redis) -> Sale | None:

    cache_key = f"sales:{sale_id}"
    cached_sale = redis.get(cache_key)

    if cached_sale:
        return sale_from_dict(simplejson.loads(cached_sale))

    sale = await session.get(Sale, sale_id)

    if sale:
        redis.set(cache_key, simplejson.dumps(sale_to_dict(sale)), ex=600)
    return sale


async def get_sale_by_date(
        session: AsyncSession,
        sale_date: date,
        redis: Redis) -> Sale | None:

    cache_key = f"sales:date:{sale_date.isoformat()}"
    cached_sale = redis.get(cache_key)

    if cached_sale:
        return sale_from_dict(simplejson.loads(cached_sale))

    stmt = select(Sale).filter(Sale.date == sale_date)
    result = await session.scalars(stmt)
    sale = result.first()

    if sale:
        redis.set(cache_key, simplejson.dumps(sale_to_dict(sale)), ex=600)
    return sale


# ------------------------------------
# POST
# ------------------------------------

async def create_sale(
        session: AsyncSession,
        sale_create: Sale) -> Sale:

    sale = Sale(**sale_create.model_dump())
    session.add(sale)

    await session.commit()
    await session.refresh(sale)

    return sale


# ------------------------------------
# PATCH
# ------------------------------------

async def update_sale(
        session: AsyncSession,
        sale: Sale,
        sale_update: Sale) -> Sale:

    for name, value in sale_update.model_dump(exclude_unset=True).items():
        setattr(sale, name, value)
    await session.commit()

    return sale


# ------------------------------------
# DELETE
# ------------------------------------

async def delete_sale(
        session: AsyncSession,
        sale: Sale) -> None:

    await session.delete(sale)
    await session.commit()
