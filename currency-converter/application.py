"""Application module."""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from . import endpoints
from .containers import Container


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Currency Converter",
        version="0.1.0",
        description="Currency converter app",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[endpoints])

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.openapi = custom_openapi
    app.container = container
    app.include_router(endpoints.currency_router)
    app.include_router(endpoints.quotation_router)
    app.include_router(endpoints.converter_router)
    return app


app = create_app()
