"""Endpoints module."""

from typing import Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, constr

from .containers import Container
from .repositories import NotFoundError
from .services import CurrencyService


class Currency(BaseModel):
    abb: constr(regex='^[A-Z]{3}$')
    name: str
    id: int


class CurrencyList(BaseModel):
    currencies: Optional[List[Currency]]


currency_router = APIRouter(tags=['currency'])


@currency_router.get('/currencies', response_model=CurrencyList)
@inject
def get_list(
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    return currency_service.get_currencies()


@currency_router.get('/currencies/{currency_id}', response_model=Currency)
@inject
def get_by_id(
        currency_id: int,
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    try:
        return currency_service.get_currency_by_id(currency_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@currency_router.post('/currencies', status_code=status.HTTP_201_CREATED)
@inject
def add(
        currency: Currency,
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    return currency_service.create_currency(currency.abb, currency.name)


@currency_router.delete('/currencies/{currency_id}', status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        currency_id: int,
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    try:
        currency_service.delete_currency_by_id(currency_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@currency_router.get('/status')
def get_status():
    return {'status': 'OK'}
