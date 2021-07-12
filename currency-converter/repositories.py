"""Repositories module."""

from contextlib import AbstractContextManager
from datetime import date, datetime
from typing import Callable, Iterator, Optional

from sqlalchemy import desc
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
            currency = session.query(Currency) \
                .filter(Currency.id == currency_id) \
                .first()

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
            entity: Currency = self.get_by_id(currency_id)
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
            entity: Currency = self.get_by_id(currency_id)
            session.delete(entity)
            session.commit()


class CurrencyQuotationRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self, currency_id: int) -> Iterator[CurrencyQuotation]:
        with self.session_factory() as session:
            return session.query(CurrencyQuotation) \
                .filter(CurrencyQuotation.currency_id == currency_id) \
                .all()

    def get_by_id(self, currency_id: int, quotation_id: int) -> CurrencyQuotation:
        with self.session_factory() as session:
            currency_quotation = session.query(CurrencyQuotation) \
                .filter(CurrencyQuotation.currency_id == currency_id, CurrencyQuotation.id == quotation_id) \
                .first()

            if not currency_quotation:
                raise NotFoundError(CurrencyQuotationRepository.__name__)

            return currency_quotation

    def get_by_abb_and_date(
            self,
            currency_abb: str,
            date: Optional[date] = None
    ) -> CurrencyQuotation:
        with self.session_factory() as session:
            res = session.query(CurrencyQuotation, Currency) \
                .join(Currency, Currency.id == CurrencyQuotation.currency_id)

            res = res.filter(Currency.abb == currency_abb)

            if date is not None:
                res = res.filter(CurrencyQuotation.date <= date)

            res = res.order_by(desc(CurrencyQuotation.date)) \
                .limit(1) \
                .first()

            if res is None:
                raise NotFoundError(CurrencyQuotationRepository.__name__)

            return CurrencyQuotation(
                id=res.CurrencyQuotation.id,
                currency_id=res.CurrencyQuotation.currency_id,
                exchange_rate=res.CurrencyQuotation.exchange_rate,
                date=res.CurrencyQuotation.date,
            )

    def add(self, currency_id: int, currency_quotation: CurrencyQuotationIn) -> CurrencyQuotation:
        with self.session_factory() as session:
            currency_quotation = CurrencyQuotation(currency_id=currency_id,
                                                   exchange_rate=currency_quotation.exchange_rate,
                                                   date=currency_quotation.date or f'{datetime.now():%Y-%m-%d}')

            try:
                session.add(currency_quotation)
                session.commit()
                session.refresh(currency_quotation)

                return currency_quotation
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def update_by_id(
            self,
            currency_id: int,
            quotation_id: int,
            currency_quotation: CurrencyQuotationIn
    ) -> CurrencyQuotation:
        with self.session_factory() as session:
            entity: CurrencyQuotation = self.get_by_id(currency_id, quotation_id)
            entity.date = currency_quotation.date or f'{datetime.now():%Y-%m-%d}'
            entity.exchange_rate = currency_quotation.exchange_rate

            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)

                return entity
            except IntegrityError as e:
                raise DataBaseIntegrityError(e)

    def delete_by_id(self, currency_id: int, quotation_id: int) -> None:
        with self.session_factory() as session:
            entity: CurrencyQuotation = self.get_by_id(currency_id, quotation_id)
            session.delete(entity)
            session.commit()


class NotFoundError(Exception):
    def __init__(self, entity_name):
        super().__init__(f'{entity_name} not found')


class DataBaseIntegrityError(Exception):
    def __init__(self, e: IntegrityError):
        super().__init__(f'DatabaseIntegrityError: {e.__cause__}')
