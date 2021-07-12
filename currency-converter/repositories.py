"""Repositories module."""

from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, Iterator

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .dtos import CurrencyIn, CurrencyQuotationIn
from .models import Currency, CurrencyQuotation


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
                raise NotFoundError(CurrencyRepository.__name__)

            return currency

    def add(self, currency: CurrencyIn) -> Currency:
        with self.session_factory() as session:
            currency = Currency(abb=currency.abb, name=currency.name)

            try:
                session.add(currency)
                session.commit()
                session.refresh(currency)

                return currency
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def update_by_id(self, currency_id: int, currency: CurrencyIn) -> Currency:
        with self.session_factory() as session:
            entity: Currency = session.query(Currency).filter(Currency.id == currency_id).first()

            if not entity:
                raise NotFoundError(CurrencyRepository.__name__)

            entity.abb = currency.abb
            entity.name = currency.name

            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)

                return entity
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def delete_by_id(self, currency_id: int) -> None:
        with self.session_factory() as session:
            entity: Currency = session.query(Currency).filter(Currency.id == currency_id).first()

            if not entity:
                raise NotFoundError(CurrencyRepository.__name__)

            session.delete(entity)
            session.commit()


class CurrencyQuotationRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self, currency_id: int) -> Iterator[CurrencyQuotation]:
        with self.session_factory() as session:
            return session.query(CurrencyQuotation).filter(CurrencyQuotation.currency_id == currency_id).all()

    def get_by_id(self, currency_id: int, quotation_id: int) -> CurrencyQuotation:
        with self.session_factory() as session:
            currency_quotation = session.query(CurrencyQuotation).filter(
                CurrencyQuotation.currency_id == currency_id, CurrencyQuotation.id == quotation_id).first()

            if not currency_quotation:
                raise NotFoundError(CurrencyQuotationRepository.__name__)

            return currency_quotation

    def add(self, currency_id: int, currency_quotation: CurrencyQuotationIn) -> CurrencyQuotation:
        with self.session_factory() as session:
            currency_quotation = CurrencyQuotation(currency_id=currency_id,
                                                   exchange_rate=currency_quotation.exchange_rate,
                                                   date=currency_quotation.date or datetime.now())

            try:
                session.add(currency_quotation)
                session.commit()
                session.refresh(currency_quotation)

                return currency_quotation
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def update_by_id(self, quotation_id: int, currency_quotation: CurrencyQuotationIn) -> CurrencyQuotation:
        with self.session_factory() as session:
            entity: CurrencyQuotation = session.query(CurrencyQuotation).filter(
                CurrencyQuotation.id == quotation_id).first()

            if not entity:
                raise NotFoundError(CurrencyQuotationRepository.__name__)

            entity.currency_id = currency_quotation.currency_id
            entity.exchange_rate = currency_quotation.exchange_rate

            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)

                return entity
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def delete_by_id(self, quotation_id: int) -> None:
        with self.session_factory() as session:
            entity: CurrencyQuotation = session.query(Currency).filter(Currency.id == quotation_id).first()

            if not entity:
                raise NotFoundError(CurrencyQuotationRepository.__name__)

            session.delete(entity)
            session.commit()


class NotFoundError(Exception):
    def __init__(self, entity_name):
        super().__init__(f'{entity_name} not found')


class DataBaseIntegrityError(Exception):
    def __init__(self, e: IntegrityError):
        super().__init__(f'DatabaseIntegrityError: {e.__cause__}')
