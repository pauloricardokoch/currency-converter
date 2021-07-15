"""Services module."""
import datetime
from typing import Iterator, Optional

from .dtos import (
    CurrencyIn, CurrencyOut, CurrencyQuotationIn,
    CurrencyQuotationOut, ConverterIn, ConverterOut
)
from .repositories import (
    CurrencyRepository, CurrencyQuotationRepository,
    NotFoundError
)


class CurrencyService:
    def __init__(self, currency_repository: CurrencyRepository) -> None:
        self._repository: CurrencyRepository = currency_repository

    def get_currencies(self) -> Iterator[CurrencyOut]:
        currencies = map(
            lambda currency: CurrencyOut(
                abb=currency.abb, name=currency.name, id=currency.id
            ),
            self._repository.get_all()
        )

        return list(currencies)

    def get_currency_by_id(self, currency_id: int) -> CurrencyOut:
        currency = self._repository.get_by_id(currency_id)

        return CurrencyOut(
            abb=currency.abb, name=currency.name, id=currency.id
        )

    def create_currency(self, currency: CurrencyIn) -> CurrencyOut:
        currency = self._repository.add(currency)

        return CurrencyOut(
            abb=currency.abb, name=currency.name, id=currency.id
        )

    def update_currency(
            self, currency_id: int, currency: CurrencyIn
    ) -> CurrencyOut:
        currency = self._repository.update_by_id(currency_id, currency)

        return CurrencyOut(
            abb=currency.abb, name=currency.name, id=currency.id
        )

    def delete_currency_by_id(self, currency_id: int) -> None:
        return self._repository.delete_by_id(currency_id)


class CurrencyQuotationService:
    def __init__(
            self, currency_quotation_repo: CurrencyQuotationRepository
    ) -> None:
        self._repository: CurrencyQuotationRepository = currency_quotation_repo

    def get_currency_quotations(self, currency_id: int) -> Iterator[
        CurrencyQuotationOut
    ]:
        currency_quotations = map(
            lambda currency_quotation: CurrencyQuotationOut(
                id=currency_quotation.id,
                currency_id=currency_quotation.currency_id,
                exchange_rate=currency_quotation.exchange_rate,
                date=currency_quotation.date
            ),
            self._repository.get_all(currency_id)
        )

        return list(currency_quotations)

    def get_currency_quotation_by_id(
            self, currency_id: int, quotation_id: int
    ) -> CurrencyQuotationOut:
        currency_quotation = self._repository.get_by_id(
            currency_id, quotation_id
        )

        return CurrencyQuotationOut(
            id=currency_quotation.id,
            currency_id=currency_quotation.currency_id,
            exchange_rate=currency_quotation.exchange_rate,
            date=currency_quotation.date
        )

    def create_currency_quotation(
            self, currency_id: int,
            currency_quotation: CurrencyQuotationIn
    ) -> CurrencyQuotationOut:
        currency_quotation = self._repository.add(
            currency_id, currency_quotation
        )

        return CurrencyQuotationOut(
            id=currency_quotation.id,
            currency_id=currency_quotation.currency_id,
            exchange_rate=currency_quotation.exchange_rate,
            date=currency_quotation.date
        )

    def update_currency_quotation(
            self, currency_id: int, quotation_id: int,
            currency_quotation: CurrencyQuotationIn
    ) -> CurrencyQuotationOut:
        currency_quotation = self._repository.update_by_id(
            currency_id, quotation_id, currency_quotation
        )

        return CurrencyQuotationOut(
            id=currency_quotation.id,
            currency_id=currency_quotation.currency_id,
            exchange_rate=currency_quotation.exchange_rate,
            date=currency_quotation.date
        )

    def delete_currency_quotation_by_id(
            self, currency_id: int, quotation_id: int
    ) -> None:
        return self._repository.delete_by_id(currency_id, quotation_id)


class CurrencyConverterService:
    def __init__(
            self, currency_quotation_repo: CurrencyQuotationRepository
    ) -> None:
        self._repository: CurrencyQuotationRepository = currency_quotation_repo

    def _get_quotation(self, currency_abb: str, date: Optional[datetime.date]):
        quotation = self._repository.get_by_abb_and_date(currency_abb, date)

        return CurrencyQuotationOut(
            id=quotation.id,
            currency_id=quotation.currency_id,
            exchange_rate=quotation.exchange_rate,
            date=quotation.date
        )

    def _get_quotation_from(
            self, currency_abb: str, date: Optional[datetime.date]
    ):
        try:
            return self._get_quotation(currency_abb, date)
        except NotFoundError:
            raise NotFoundError('QuotationFrom not found in the database')

    def _get_quotation_to(
            self, currency_abb: str, date: Optional[datetime.date]
    ):
        try:
            return self._get_quotation(currency_abb, date)
        except NotFoundError:
            raise NotFoundError('QuotationTo not found in the database')

    def convert_currency(self, converter: ConverterIn) -> ConverterOut:
        quotation_from = self._get_quotation_from(
            converter.currency_abb_from, converter.date
        )
        quotation_to = self._get_quotation_to(
            converter.currency_abb_to, converter.date
        )

        rate = quotation_from.exchange_rate / quotation_to.exchange_rate
        value = round(converter.value * rate, 3)

        return ConverterOut(
            CurrencyQuotationFrom=quotation_from,
            CurrencyQuotationTo=quotation_to,
            value=value
        )
