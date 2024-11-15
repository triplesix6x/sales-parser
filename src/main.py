from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from core.config import settings
from api.v1 import router as api_v1_router
from contextlib import asynccontextmanager
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    yield

    # Shutdown
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse)
app.include_router(api_v1_router)


def main():
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config="log_conf.yaml")


if __name__ == "__main__":
    main()
