import typing

from fastapi import APIRouter, FastAPI


class RouterBuilder:
    def __init__(self):
        self._router = APIRouter(prefix="/api")

    def with_router(self, router: APIRouter) -> typing.Self:
        self._router.include_router(router)
        return self

    def build(self) -> APIRouter:
        return self._router


class DependencyInjector:
    def __init__(self, *args, **kwargs):
        self._app = FastAPI(*args, **kwargs)

    def with_dependency(
        self, interface: typing.Callable, implementation: typing.Callable
    ) -> typing.Self:
        self._app.dependency_overrides[interface] = implementation
        return self

    def build_app(self) -> FastAPI:
        return self._app
