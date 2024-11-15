from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from core.models import db_helper, redis_helper
from redis import Redis
from .schemas import SaleRead
from . import crud


async def get_sale_by_id(
        sale_id: Annotated[int, Path(ge=1)],
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        redis: Annotated[Redis, Depends(redis_helper.get_redis)]) -> SaleRead:

    sale = await crud.get_sale(
        session=session,
        sale_id=sale_id,
        redis=redis)

    if sale:
        return sale

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sale {sale_id} not found!")


async def get_sale_by_date(
        sale_date: date,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        redis: Annotated[Redis, Depends(redis_helper.get_redis)]) -> SaleRead:

    sale = await crud.get_sale_by_date(
        session=session,
        sale_date=sale_date,
        redis=redis)

    if sale:
        return sale

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sale dated {sale_date} not found!")
