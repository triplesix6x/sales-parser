from fastapi import APIRouter, Depends, status
from typing import Annotated
from core.config import settings
from core.models import db_helper
from .schemas import ProductRead, ProductCreate, ProductDelete, ProductUpdate
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import get_product_by_id, get_products_by_sale_id, get_products_by_sale_date

router = APIRouter(
    prefix=settings.api_prefix.v1.products,
    tags=["Products"])


# --------------------------------
# GET
# --------------------------------


@router.get("/", response_model=list[ProductRead])
async def get_products(
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]):

    products = await crud.get_all_products(
        session=session)

    return products


@router.get("/id/{product_id}/", response_model=ProductRead)
async def get_product(
        product: ProductRead = Depends(get_product_by_id)):
    return product


@router.get("/sale_id/{sale_id}/", response_model=list[ProductRead])
async def get_products_by_sale_id(
        products: list[ProductRead] = Depends(get_products_by_sale_id)):
    return products


@router.get("/sale_date/{sale_date}/", response_model=list[ProductRead])
async def get_products_by_sale_id(
        products: list[ProductRead] = Depends(get_products_by_sale_date)):
    return products


# --------------------------------
# POST
# --------------------------------


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_create: ProductCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],):

    product = await crud.create_product(
        session=session,
        product_create=product_create)

    return product


# --------------------------------
# PATCH
# --------------------------------


@router.patch("/{product_id}/", response_model=ProductRead)
async def update_product(
        product_update: ProductUpdate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        product: ProductUpdate = Depends(get_product_by_id),):

    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update)


# --------------------------------
# DELETE
# --------------------------------


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        product: ProductDelete = Depends(get_product_by_id)):

    return await crud.delete_product(
        session=session,
        product=product)
