from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from core.models import Sale


# ------------------------------------
# GET
# ------------------------------------

async def get_all_sales(
        session: AsyncSession) -> Sequence[Sale]:

    stmt = select(Sale).order_by(Sale.id.desc())
    result = await session.scalars(stmt)

    return result.all()


async def get_sale(
        session: AsyncSession,
        sale_id: int) -> Sale | None:

    return await session.get(Sale, sale_id)


async def get_sale_by_date(
        session: AsyncSession,
        sale_date: date) -> Sale | None:

    stmt = select(Sale).where(Sale.date == sale_date)
    result = await session.scalars(stmt)
    return result.first()

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
