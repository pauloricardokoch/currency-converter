"""Models module."""

from sqlalchemy import Column, String, Integer

from .database import Base


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    abb = Column(String, unique=True)
    name = Column(String)

    def __repr__(self):
        return f'<Currency(id="{self.id}", ' \
               f'abb="{self.abb}"), ' \
               f'name="{self.name}")>'
