from src.common.config import Config
from src.common.fastapi_utils import DependencyInjector, RouterBuilder
from src.common.s3 import S3Gateway, get_local_s3_gateway
from src.common.sql import SQLDatabase
from src.products.api import router as products_router

config = Config()
sql_database = SQLDatabase()

dependency_injector = DependencyInjector(
    title="Bazar API", swagger_ui_parameters={"displayRequestDuration": True}
).with_dependency(SQLDatabase, sql_database)

if config.enable_local_aws_emulation:
    dependency_injector = dependency_injector.with_dependency(
        S3Gateway, get_local_s3_gateway
    )

app = dependency_injector.build_app()

app.include_router(RouterBuilder().with_router(products_router).build())
