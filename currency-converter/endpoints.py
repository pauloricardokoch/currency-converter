"""Endpoints module."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, constr

from .containers import Container
from .repositories import NotFoundError
from .services import CurrencyService


class Currency(BaseModel):
    abb = constr(regex='^[A-Z]{3}$')
    name = str
    id = int


router = APIRouter()


@router.get('/currencies')
@inject
def get_list(
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    return currency_service.get_currencies()


@router.get('/currencies/{currency_id}')
@inject
def get_by_id(
        currency_id: int,
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    try:
        return currency_service.get_currency_by_id(currency_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/currencies', status_code=status.HTTP_201_CREATED)
@inject
def add(
        currency: Currency,
        currency_service: CurrencyService = Depends(Provide[Container.currency_service]),
):
    return currency_service.create_currency(currency.abb, currency.name)


@router.delete('/currencies/{currency_id}', status_code=status.HTTP_204_NO_CONTENT)
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


@router.get('/status')
def get_status():
    return {'status': 'OK'}
