import datetime

from pydantic import BaseModel, constr
from typing import Optional


class CurrencyIn(BaseModel):
    abb: constr(regex='^[A-Z]{3}$')
    name: str


class CurrencyOut(BaseModel):
    abb: constr(regex='^[A-Z]{3}$')
    name: str
    id: int


class CurrencyQuotationIn(BaseModel):
    exchange_rate: float
    date: Optional[datetime.datetime]


class CurrencyQuotationOut(BaseModel):
    currency_id: int
    exchange_rate: float
    date: Optional[datetime.datetime]
    id: int
