from decimal import Decimal

import alembic.config
from alembic import config, command
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncConnection

from src.common.config import Config
from src.common.sql import create_database_engine, dispose_engine, get_session_factory, connection_string_from_config
from src.common.time import LocalTimeProvider
from src.products.service import ProductService
from src.products.dto import ProductWrite, NewTag, CategoryWrite, BrandWrite, TagItem, CategoryItem, BrandItem, ProductDetail


def migrate(connection: AsyncConnection, alembic_config: alembic.config.Config) -> None:
    alembic_config.attributes["connection"] = connection
    command.upgrade(alembic_config, "head")


def downgrade(connection: AsyncConnection, alembic_config: alembic.config.Config) -> None:
    alembic_config.attributes["connection"] = connection
    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
async def database() -> async_sessionmaker:
    config_ = Config()
    dns = connection_string_from_config(config_)
    engine = create_database_engine(dns)

    alembic_config = alembic.config.Config()
    alembic_config.set_main_option("script_location", "alembic")
    async with engine.begin() as connection:
        migrate(connection, alembic_config)

    session_factory = get_session_factory(engine)
    yield session_factory

    async with engine.begin() as connection:
        downgrade(connection, alembic_config)

    await dispose_engine(engine)


@pytest.fixture(scope="function")
async def service(database) -> ProductService:
    return ProductService(database, LocalTimeProvider())


async def add_tag(tag: str, service: ProductService) -> TagItem:
    result = await service.add_tag(NewTag(tag=tag))
    return result.tag


async def add_brand(name: str, logo_url: str, service: ProductService) -> BrandItem:
    result = await service.add_brand(
        BrandWrite(name=name, logo_url=logo_url)
    )
    return result.brand


async def add_category(category: str, service: ProductService) -> CategoryItem:
    result = await service.create_category(CategoryWrite(name=category))
    return result.category


async def add_sample_product(service: ProductService) -> ProductDetail:
    tag = await add_tag("Vegetables", service)
    brand = await add_brand("Farmary", "https://s3.eu-central-1.amazonaws.com/bucket/file", service)
    category = await add_category("Vegetables", service)
    result = await service.add_product(
        ProductWrite(
            sku="2,51,594",
            name="Chinese Cabbage",
            image_url="https://s3.eu-central-1.amazonaws.com/bucket/file",
            description="Sed commodo aliquam dui ac porta. Fusce ipsum felis,"
                        " imperdiet at posuere ac, viverra at mauris (...)",
            base_price=Decimal("48.00"),
            discount=64,
            quantity=5413,
            weight=3,
            color="Green",
            tags_guids=[tag.guid],
            category_guid=category.guid,
            brand_guid=brand.guid
        )
    )
    return result.product


async def test_product_added(service: ProductService):
    # GIVEN clean state
    # WHEN a product is added
    product = await add_sample_product(service)
    # THEN it can be retrieved
    result = await service.get_product_details(product.guid)
    assert result.guid == product.guid

