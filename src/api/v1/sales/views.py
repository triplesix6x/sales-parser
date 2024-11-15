from fastapi import APIRouter, Depends, status
from typing import Annotated
from core.config import settings
from core.models import db_helper
from .schemas import SaleRead, SaleCreate, SaleDelete, SaleUpdate
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import get_sale_by_id, get_sale_by_date

router = APIRouter(
    prefix=settings.api_prefix.v1.sales,
    tags=["Sales"])


# --------------------------------
# GET
# --------------------------------


@router.get("/", response_model=list[SaleRead])
async def get_sales(
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]):

    sales = await crud.get_all_sales(
        session=session)

    return sales


@router.get("/date/{sale_date}/", response_model=SaleRead)
async def get_sale_by_date(
        sale: SaleRead = Depends(get_sale_by_date)):
    return sale


@router.get("/id/{sale_id}/", response_model=SaleRead)
async def get_sale(
        sale: SaleRead = Depends(get_sale_by_id)):
    return sale


@router.get("/report/{sale_date}/", response_model=str)
async def get_sale_report_by_date(
        sale: SaleRead = Depends(get_sale_by_date)):
    return sale.report
# --------------------------------
# POST
# --------------------------------


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
async def create_sale(
        sale_create: SaleCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],):

    sale = await crud.create_sale(
        session=session,
        sale_create=sale_create)

    return sale


# --------------------------------
# PATCH
# --------------------------------


@router.patch("/{sale_id}/", response_model=SaleRead)
async def update_sale(
        sale_update: SaleUpdate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        sale: SaleUpdate = Depends(get_sale_by_id),):

    return await crud.update_sale(
        session=session,
        sale=sale,
        sale_update=sale_update)


# --------------------------------
# DELETE
# --------------------------------


@router.delete("/{sale_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        sale: SaleDelete = Depends(get_sale_by_id)):

    return await crud.delete_sale(
        session=session,
        sale=sale)
