from typing import Annotated, Sequence
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Product, redis_helper
from datetime import date
from redis import Redis
from . import crud


async def get_product_by_id(
        product_id: Annotated[int, Path(ge=1)],
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        redis: Annotated[Redis, Depends(redis_helper.get_redis)]) -> Product:

    product = await crud.get_product(
        session=session,
        product_id=product_id,
        redis=redis)

    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!")


async def get_products_by_sale_id(
        sale_id: Annotated[int, Path(ge=1)],
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        redis: Annotated[Redis, Depends(redis_helper.get_redis)]) -> Sequence[Product]:

    products = await crud.get_products_by_sale_id(
        session=session,
        sale_id=sale_id,
        redis=redis)

    if products:
        return products

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Products from {sale_id} not found!")


async def get_products_by_sale_date(
        sale_date: date,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        redis: Annotated[Redis, Depends(redis_helper.get_redis)]) -> Sequence[Product]:

    products = await crud.get_products_by_sale_date(
        session=session,
        sale_date=sale_date,
        redis=redis)

    if products:
        return products

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Products dated {sale_date} not found!")
