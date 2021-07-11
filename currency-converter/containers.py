"""Containers module."""

from dependency_injector import containers, providers

from .database import Database
from .repositories import CurrencyRepository
from .services import CurrencyService


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
