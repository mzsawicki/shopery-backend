import taskiq_fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.common.config import Config
from src.common.cors import parse_origins
from src.common.fastapi_utils import DependencyInjector, RouterBuilder
from src.common.s3 import ObjectStorageGateway, get_local_s3_gateway
from src.common.tasks import broker
from src.products.api import router as products_router
from src.store.api import router as store_router

config = Config()

dependency_injector = DependencyInjector(
    title="Bazar API", swagger_ui_parameters={"displayRequestDuration": True}
)

if config.enable_local_aws_emulation:
    dependency_injector = dependency_injector.with_dependency(
        ObjectStorageGateway, get_local_s3_gateway
    )

app = dependency_injector.build_app()

app.include_router(
    RouterBuilder()
    .with_router(products_router)
    .with_router(store_router)
    .build()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_origins(config.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_startup():
    if not broker.is_worker_process:
        await broker.startup()


@app.on_event("shutdown")
async def app_shutdown():
    if not broker.is_worker_process:
        await broker.shutdown()


taskiq_fastapi.init(broker, "src.api:app")
