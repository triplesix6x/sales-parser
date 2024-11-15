from pydantic import BaseModel, ConfigDict
from datetime import date as _date


class SaleBase(BaseModel):
    date: _date
    report: str


class SaleCreate(SaleBase):
    pass


class SaleDelete(SaleBase):
    pass


class SaleRead(SaleBase):
    model_config = ConfigDict(
        from_attributes=True)
    id: int


class SaleUpdate(SaleBase):
    date: _date | None = None
    report: str | None = None
