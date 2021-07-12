from datetime import date
from typing import Optional

from pydantic import BaseModel, constr


class CurrencyIn(BaseModel):
    abb: constr(regex='^[A-Z]{3}$')
    name: str


class CurrencyOut(BaseModel):
    abb: constr(regex='^[A-Z]{3}$')
    name: str
    id: int


class CurrencyQuotationIn(BaseModel):
    exchange_rate: float
    date: Optional[date]


class CurrencyQuotationOut(BaseModel):
    currency_id: int
    exchange_rate: float
    date: Optional[date]
    id: int


class ConverterIn(BaseModel):
    currency_id_from: int
    currency_id_to: int
    date: Optional[date]
    value: float


class ConverterOut(BaseModel):
    CurrencyQuotationFrom: CurrencyQuotationOut
    CurrencyQuotationTo: CurrencyQuotationOut
    value: float
