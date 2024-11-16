from api.v1.products import crud
import pytest
from unittest.mock import AsyncMock, patch
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis


@pytest.mark.asyncio
@patch("api.v1.products.crud.get_product")
@patch("core.models.redis_helper.redis_helper.get_redis")
@patch("core.models.db_helper.db_helper.session_dependency")
async def test_get_product(mock_session_dependency, mock_get_redis, mock_get_product):
    test_product_id = 1
    test_product = {
        "id": test_product_id,
        "name": "Test Product",
        "quantity": 10,
        "price": "99.99",
        "category": "Electronics",
        "sale_id": 2
    }

    mock_redis = AsyncMock(spec=Redis)
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_dependency.return_value = mock_session

    mock_get_product.return_value = test_product

    result = await crud.get_product(
        session=mock_session,
        product_id=test_product_id,
        redis=mock_redis
    )

    assert result == test_product

    mock_get_product.assert_awaited_once_with(
        session=mock_session, product_id=test_product_id, redis=mock_redis
    )


@pytest.mark.asyncio
@patch("api.v1.products.crud.get_products_by_sale_id")
@patch("core.models.redis_helper.redis_helper.get_redis")
@patch("core.models.db_helper.db_helper.session_dependency")
async def test_get_products_by_sale_id(mock_session_dependency, mock_get_redis, mock_get_products_by_sale_id):
    test_sale_id = 1
    test_products = [
        {
            "id": 1,
            "name": "Product A",
            "quantity": 5,
            "price": "50.00",
            "category": "Furniture",
            "sale_id": test_sale_id
        },
        {
            "id": 2,
            "name": "Product B",
            "quantity": 3,
            "price": "150.00",
            "category": "Appliances",
            "sale_id": test_sale_id
        },
    ]

    mock_redis = AsyncMock(spec=Redis)
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_dependency.return_value = mock_session

    mock_get_products_by_sale_id.return_value = test_products

    result = await crud.get_products_by_sale_id(
        session=mock_session,
        sale_id=test_sale_id,
        redis=mock_redis
    )

    assert result == test_products

    mock_get_products_by_sale_id.assert_awaited_once_with(
        session=mock_session, sale_id=test_sale_id, redis=mock_redis
    )


@pytest.mark.asyncio
@patch("api.v1.products.crud.get_products_by_sale_date")
@patch("core.models.redis_helper.redis_helper.get_redis")
@patch("core.models.db_helper.db_helper.session_dependency")
async def test_get_products_by_sale_date(mock_session_dependency, mock_get_redis, mock_get_products_by_sale_date):
    test_sale_date = date(2024, 11, 15)
    test_products = [
        {
            "id": 1,
            "name": "Product A",
            "quantity": 5,
            "price": "50.00",
            "category": "Furniture",
            "sale_id": 2
        },
        {
            "id": 2,
            "name": "Product B",
            "quantity": 3,
            "price": "150.00",
            "category": "Appliances",
            "sale_id": 2
        },
    ]

    mock_redis = AsyncMock(spec=Redis)
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_dependency.return_value = mock_session

    mock_get_products_by_sale_date.return_value = test_products

    result = await crud.get_products_by_sale_date(
        session=mock_session,
        sale_date=test_sale_date,
        redis=mock_redis
    )

    assert result == test_products

    mock_get_products_by_sale_date.assert_awaited_once_with(
        session=mock_session, sale_date=test_sale_date, redis=mock_redis
    )
