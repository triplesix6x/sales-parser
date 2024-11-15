from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from core.config import settings
from api.v1 import router as api_v1_router
from contextlib import asynccontextmanager
from core.models import db_helper, redis_helper
from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    yield

    # Shutdown
    await db_helper.dispose()
    redis_helper.disconnect_from_redis()


app = FastAPI(
    default_response_class=ORJSONResponse)
app.include_router(api_v1_router)


Instrumentator().instrument(app).expose(app)


def main():
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config="log_conf.yaml")


if __name__ == "__main__":
    main()
