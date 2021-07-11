"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from .models import Currency


class CurrencyRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Currency]:
        with self.session_factory() as session:
            return session.query(Currency).all()

    def get_by_id(self, currency_id: int) -> Currency:
        with self.session_factory() as session:
            currency = session.query(Currency).filter(Currency.id == currency_id).first()
            if not currency:
                raise CurrencyNotFoundError(currency_id)
            return currency

    def add(self, abb: str, name: str) -> Currency:
        with self.session_factory() as session:
            currency = Currency(abb=abb, name=name)
            session.add(currency)
            session.commit()
            session.refresh(currency)
            return currency

    def delete_by_id(self, currency_id: int) -> None:
        with self.session_factory() as session:
            entity: Currency = session.query(Currency).filter(Currency.id == currency_id).first()
            if not entity:
                raise CurrencyNotFoundError(currency_id)
            session.delete(entity)
            session.commit()


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class CurrencyNotFoundError(NotFoundError):
    entity_name: str = 'Currency'
