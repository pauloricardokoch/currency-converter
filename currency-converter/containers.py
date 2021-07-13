"""Containers module."""

from dependency_injector import containers, providers

from .database import Database
from .repositories import CurrencyRepository, CurrencyQuotationRepository
from .services import (
    CurrencyService, CurrencyQuotationService,
    CurrencyConverterService
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    currency_repository = providers.Factory(
        CurrencyRepository,
        session_factory=db.provided.session,
    )

    currency_service = providers.Factory(
        CurrencyService,
        currency_repository=currency_repository,
    )

    currency_quotation_repository = providers.Factory(
        CurrencyQuotationRepository,
        session_factory=db.provided.session,
    )

    currency_quotation_service = providers.Factory(
        CurrencyQuotationService,
        currency_quotation_repository=currency_quotation_repository,
    )

    currency_converter_service = providers.Factory(
        CurrencyConverterService,
        currency_quotation_repository=currency_quotation_repository,
    )
