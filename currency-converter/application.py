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

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()
