"""Application module."""

from fastapi import FastAPI

from . import endpoints
from .containers import Container


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[endpoints])

    db = container.db()
    db.create_database()

    fastapi_app = FastAPI()
    fastapi_app.container = container
    fastapi_app.include_router(endpoints.currency_router)
    return fastapi_app


app = create_app()
