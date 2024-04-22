import typing
import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, async_sessionmaker

import alembic.config
from alembic import command
from src.common.config import Config
from src.common.sql import (connection_string_from_config,
                            create_database_engine, dispose_engine,
                            get_session_factory)
from src.common.time import LocalTimeProvider
from src.products.dto import BrandWrite, CategoryWrite, NewTag, ProductWrite
from src.products.service import ProductService


def migrate(connection: AsyncConnection, alembic_config: alembic.config.Config) -> None:
    alembic_config.attributes["connection"] = connection
    command.upgrade(alembic_config, "head")


def downgrade(
    connection: AsyncConnection, alembic_config: alembic.config.Config
) -> None:
    alembic_config.attributes["connection"] = connection
    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
async def database() -> typing.AsyncGenerator[async_sessionmaker, None]:
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


def tag_green() -> NewTag:
    return NewTag(tag="green")


def category_vegetables() -> CategoryWrite:
    return CategoryWrite(name="Vegetables")


def brand_farmery() -> BrandWrite:
    return BrandWrite(
        name="Farmery", logo_url="https://s3.eu-central-1.amazonaws.com/bucket/file"
    )


def product_chinese_cabbage_sku_2_51_594(
    tags_guids: typing.List[uuid.UUID], category_guid: uuid.UUID, brand_guid: uuid.UUID
) -> ProductWrite:
    return ProductWrite(
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
        tags_guids=tags_guids,
        category_guid=category_guid,
        brand_guid=brand_guid,
    )


def product_chinese_cabbage_sku_3_62_605(
    tags_guids: typing.List[uuid.UUID], category_guid: uuid.UUID, brand_guid: uuid.UUID
):
    return ProductWrite(
        sku="3,62,605",
        name="Chinese Cabbage",
        image_url="https://s3.eu-central-1.amazonaws.com/bucket/file",
        description="Sed commodo aliquam dui ac porta. Fusce ipsum felis,"
        " imperdiet at posuere ac, viverra at mauris (...)",
        base_price=Decimal("48.00"),
        discount=64,
        quantity=5413,
        weight=3,
        color="Green",
        tags_guids=tags_guids,
        category_guid=category_guid,
        brand_guid=brand_guid,
    )


def product_green_chili_sku_2_51_594(
    tags_guids: typing.List[uuid.UUID], category_guid: uuid.UUID, brand_guid: uuid.UUID
) -> ProductWrite:
    return ProductWrite(
        sku="2,51,594",
        name="Green Chili",
        image_url="https://s3.eu-central-1.amazonaws.com/bucket/file",
        description="Sed commodo aliquam dui ac porta. Fusce ipsum felis,"
        " imperdiet at posuere ac, viverra at mauris (...)",
        base_price=Decimal("10.00"),
        discount=10,
        quantity=6000,
        weight=1,
        color="Green",
        tags_guids=tags_guids,
        category_guid=category_guid,
        brand_guid=brand_guid,
    )


async def test_product_added(service: ProductService):
    # GIVEN clean state
    # WHEN a product is added
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    product = await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    assert product.product
    # THEN it can be retrieved
    result = await service.get_product_details(product.product.guid)
    assert result and result.guid == product.product.guid


async def test_products_cannot_have_the_same_sku(service: ProductService):
    # GIVEN a product existing
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    # WHEN there is an attempt to add another product with the same sku
    product = await service.add_product(
        product_green_chili_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    assert product.product
    # THEN the new product is not added
    assert not product.success


async def test_products_cannot_have_the_same_name(service: ProductService):
    # GIVEN a product existing
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    # WHEN there is an attempt to add another product with the same name
    product = await service.add_product(
        product_chinese_cabbage_sku_3_62_605(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    # THEN the new product is not added
    assert not product.success


async def test_product_cannot_have_nonexistent_tags(service: ProductService):
    # GIVEN clean state
    # WHEN there is attempt to add a product with non-existent tag
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    product = await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [tag.tag.guid, uuid.uuid4()], category.category.guid, brand.brand.guid
        )
    )
    # THEN it fails
    assert not product.success


async def test_product_updates(service: ProductService):
    # GIVEN a product existing
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    product = await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    assert product.product
    # WHEN a product manager updates the product's data
    product_after_update = await service.update_product(
        product.product.guid,
        product_chinese_cabbage_sku_3_62_605(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        ),
    )
    assert product_after_update.product
    # THEN the change is reflected
    assert product_after_update.product.sku == "3,62,605"


async def test_product_deletes(service: ProductService):
    # GIVEN a product existing
    tag = await service.add_tag(tag_green())
    assert tag.tag
    brand = await service.add_brand(brand_farmery())
    assert brand.brand
    category = await service.add_category(category_vegetables())
    assert category.category
    product = await service.add_product(
        product_chinese_cabbage_sku_2_51_594(
            [
                tag.tag.guid,
            ],
            category.category.guid,
            brand.brand.guid,
        )
    )
    assert product.product
    # WHEN the product is removed
    await service.remove_product(product.product.guid)
    found_product = await service.get_product_details(product.product.guid)
    # THEN it can be found no more
    assert not found_product
