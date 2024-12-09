from fastapi import APIRouter
from core.config import settings
from .sales.views import router as sales_router
from .products.views import router as products_router

router = APIRouter(prefix=settings.api_prefix.v1.prefix)
router.include_router(sales_router)
router.include_router(products_router)


@router.get("/")
async def get_api():
    return {"message": "Тест"}
