"""Models module."""

from sqlalchemy import Column, String, Integer, Float, ForeignKeyConstraint, DateTime, UniqueConstraint

from .database import Base


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    abb = Column(String, unique=True)
    name = Column(String)

    def __repr__(self):
        return f'<Currency(id="{self.id}", ' \
               f'abb="{self.abb}", ' \
               f'name="{self.name}")>'


class CurrencyQuotation(Base):
    __tablename__ = 'currency_quotation'
    __table_args__ = (
        UniqueConstraint('currency_id', 'date'),
        ForeignKeyConstraint(['currency_id'], ['currency.id'])
    )

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer)
    exchange_rate = Column(Float(precision=3))
    date = Column(DateTime)

    def __repr__(self):
        return f'<CurrencyQuotation(id="{self.id}", ' \
               f'currency_id="{self.currency_id}", ' \
               f'exchange_rate="{self.exchange_rate}", ' \
               f'date="{self.date}")>'
