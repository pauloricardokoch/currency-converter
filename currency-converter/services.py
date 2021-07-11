"""Services module."""

from typing import Iterator

from .models import Currency
from .repositories import CurrencyRepository


class CurrencyService:
    def __init__(self, currency_repository: CurrencyRepository) -> None:
        self._repository: CurrencyRepository = currency_repository

    def get_currencies(self) -> Iterator[Currency]:
        return self._repository.get_all()

    def get_currency_by_id(self, currency_id: int) -> Currency:
        return self._repository.get_by_id(currency_id)

    def create_currency(self, abb, name) -> Currency:
        return self._repository.add(abb, name)

    def delete_currency_by_id(self, currency_id: int) -> None:
        return self._repository.delete_by_id(currency_id)
