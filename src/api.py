from src.common.fastapi_utils import DependencyInjector, RouterBuilder
from src.common.sql import SQLDatabase
from src.products.api import router as products_router

sql_database = SQLDatabase()

app = (
    DependencyInjector(
        title="Bazar API", swagger_ui_parameters={"displayRequestDuration": True}
    )
    .with_dependency(SQLDatabase, sql_database)
    .build_app()
)

app.include_router(RouterBuilder().with_router(products_router).build())
