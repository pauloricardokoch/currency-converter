"""Database module."""

import logging
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import create_engine, orm, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._event()
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()

        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

    def _event(self):
        event.listen(self._engine, 'connect', self._fk_pragma_on_connect)

    @staticmethod
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')
