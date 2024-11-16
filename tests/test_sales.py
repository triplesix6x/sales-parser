from api.v1.sales import crud
import pytest
from unittest.mock import AsyncMock, patch
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis


@pytest.mark.asyncio
@patch("api.v1.sales.crud.get_sale")
@patch("core.models.redis_helper.redis_helper.get_redis")
@patch("core.models.db_helper.db_helper.session_dependency")
async def test_get_sale(mock_session_dependency, mock_get_redis, mock_get_sale):
    test_id = 1
    test_sale = {
        "id": 2,
        "date": "2024-11-15",
        "report": "Test sale report"
    }

    mock_redis = AsyncMock(spec=Redis)
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_dependency.return_value = mock_session

    mock_get_sale.return_value = test_sale

    result = await crud.get_sale(
        session=mock_session,
        sale_id=test_id,
        redis=mock_redis
    )

    assert result == test_sale

    mock_get_sale.assert_awaited_once_with(
        session=mock_session, sale_id=test_id, redis=mock_redis
    )


@pytest.mark.asyncio
@patch("api.v1.sales.crud.get_sale_by_date")
@patch("core.models.redis_helper.redis_helper.get_redis")
@patch("core.models.db_helper.db_helper.session_dependency")
async def test_get_sale_by_date(mock_session_dependency, mock_get_redis, mock_get_sale_by_date):
    test_date = date(2024, 1, 1)
    test_sale = {
        "date": test_date.isoformat(),
        "report": "Test sale report"
    }

    mock_redis = AsyncMock(spec=Redis)
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_dependency.return_value = mock_session

    mock_get_sale_by_date.return_value = test_sale

    result = await crud.get_sale_by_date(
        session=mock_session,
        sale_date=test_date,
        redis=mock_redis
    )

    assert result == test_sale

    mock_get_sale_by_date.assert_awaited_once_with(
        session=mock_session, sale_date=test_date, redis=mock_redis
    )
