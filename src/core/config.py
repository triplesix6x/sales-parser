from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pythonjsonlogger import jsonlogger
import logging
from copy import copy


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 6099


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    sales: str = "/sales"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="_",
        env_prefix="FASTAPI_",
        env_file=(".env.template", ".env"))
    run: RunConfig = RunConfig()
    api_prefix: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()


class UvicornJSONAccessFormatter(jsonlogger.JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        client_addr, method, full_path, http_version, status_code = recordcopy.args
        recordcopy.__dict__.update(
            {
                "client_addr": client_addr,
                "method": method,
                "full_path": full_path,
                "http_version": http_version,
                "status_code": status_code,
            }
        )
        return super().format(record=recordcopy)