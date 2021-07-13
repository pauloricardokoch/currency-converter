"""Endpoints module."""

from typing import Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import PlainTextResponse

from .containers import Container
from .dtos import (
    CurrencyIn, CurrencyOut, CurrencyQuotationIn,
    CurrencyQuotationOut, ConverterIn, ConverterOut
)
from .repositories import NotFoundError, DataBaseIntegrityError
from .services import (
    CurrencyService, CurrencyQuotationService,
    CurrencyConverterService
)

currency_router = APIRouter(tags=['currency'])
quotation_router = APIRouter(tags=['currency_quotation'])
converter_router = APIRouter(tags=['converter'])


@currency_router.get('/currencies', response_model=Optional[List[CurrencyOut]])
@inject
def get_list(
        currency_service: CurrencyService = Depends(
            Provide[Container.currency_service]
        ),
):
    return currency_service.get_currencies()


@currency_router.get('/currencies/{currency_id}', response_model=CurrencyOut)
@inject
def get_by_id(
        currency_id: int,
        currency_service: CurrencyService = Depends(
            Provide[Container.currency_service]
        ),
):
    try:
        return currency_service.get_currency_by_id(currency_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@currency_router.post(
    '/currencies', status_code=status.HTTP_201_CREATED,
    response_model=CurrencyOut
)
@inject
def add(
        currency: CurrencyIn,
        currency_service: CurrencyService = Depends(
            Provide[Container.currency_service]
        ),
):
    try:
        return currency_service.create_currency(currency)
    except DataBaseIntegrityError as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )


@currency_router.put('/currencies/{currency_id}', response_model=CurrencyOut)
@inject
def update(
        currency_id: int,
        currency: CurrencyIn,
        currency_service: CurrencyService = Depends(
            Provide[Container.currency_service]
        ),
):
    try:
        return currency_service.update_currency(currency_id, currency)
    except DataBaseIntegrityError as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@currency_router.delete(
    '/currencies/{currency_id}', status_code=status.HTTP_204_NO_CONTENT
)
@inject
def remove(
        currency_id: int,
        currency_service: CurrencyService = Depends(
            Provide[Container.currency_service]
        ),
):
    try:
        currency_service.delete_currency_by_id(currency_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@quotation_router.get(
    '/currencies/{currency_id}/quotations',
    response_model=Optional[List[CurrencyQuotationOut]]
)
@inject
def get_list(
        currency_id: int,
        currency_quotation_service: CurrencyQuotationService = Depends(
            Provide[Container.currency_quotation_service]
        ),
):
    return currency_quotation_service.get_currency_quotations(currency_id)


@quotation_router.get(
    '/currencies/{currency_id}/quotations/{quotation_id}',
    response_model=CurrencyQuotationOut
)
@inject
def get_by_id(
        currency_id: int,
        quotation_id: int,
        currency_quotation_service: CurrencyQuotationService = Depends(
            Provide[Container.currency_quotation_service]
        ),
):
    try:
        return currency_quotation_service.get_currency_quotation_by_id(
            currency_id, quotation_id
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@quotation_router.post(
    '/currencies/{currency_id}/quotations',
    status_code=status.HTTP_201_CREATED,
    response_model=CurrencyQuotationOut
)
@inject
def add(
        currency_id: int,
        currency_quotation: CurrencyQuotationIn,
        currency_quotation_service: CurrencyQuotationService = Depends(
            Provide[Container.currency_quotation_service]
        ),
):
    try:
        return currency_quotation_service.create_currency_quotation(
            currency_id, currency_quotation
        )
    except DataBaseIntegrityError as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )


@quotation_router.put(
    '/currencies/{currency_id}/quotations', response_model=CurrencyQuotationOut
)
@inject
def update(
        currency_id: int,
        quotation_id: int,
        currency_quotation: CurrencyQuotationIn,
        currency_quotation_service: CurrencyQuotationService = Depends(
            Provide[Container.currency_quotation_service]
        ),
):
    try:
        return currency_quotation_service.update_currency_quotation(
            currency_id, quotation_id, currency_quotation
        )
    except DataBaseIntegrityError as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@quotation_router.delete(
    '/currencies/{currency_id}/quotations',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def remove(
        currency_id: int,
        quotation_id: int,
        currency_quotation_service: CurrencyQuotationService = Depends(
            Provide[Container.currency_quotation_service]
        ),
):
    try:
        currency_quotation_service.delete_currency_quotation_by_id(
            currency_id, quotation_id
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@converter_router.post('/converter', response_model=ConverterOut)
@inject
def converter(
        converter_in: ConverterIn,
        currency_converter_service: CurrencyConverterService = Depends(
            Provide[Container.currency_converter_service]
        ),
):
    try:
        return currency_converter_service.convert_currency(converter_in)
    except DataBaseIntegrityError as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return PlainTextResponse(
            str(e), status_code=status.HTTP_400_BAD_REQUEST
        )
