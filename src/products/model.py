import datetime
import typing
import uuid
from decimal import Decimal

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        Text, UniqueConstraint)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.model import AMOUNT_NUMERIC_PRECISION, Entity

SCHEMA = "products"


class Brand(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    logo_url: Mapped[typing.Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(name, removed_at, name="unique_brand_name")

    __tablename__ = "brands"
    __table_args__ = {"schema": SCHEMA}

    def __init__(
        self, name: str, logo_url: typing.Optional[str], created_at: datetime.datetime
    ):
        self.guid: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.logo_url: str = logo_url
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at


class Category(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(name, removed_at, name="unique_category_name")

    __tablename__ = "categories"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, name: str, created_at: datetime.datetime):
        self.guid: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at


class Tag(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    tag: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(tag, removed_at, name="unique_tag")

    __tablename__ = "tags"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, tag: str, created_at: datetime.datetime):
        self.guid: uuid.UUID = uuid.uuid4()
        self.tag: str = tag
        self.created_at: datetime.datetime = created_at


products_tags = Table(
    "products_tags",
    Entity.metadata,
    Column("tag_guid", ForeignKey("products.tags.guid")),
    Column("product_guid", ForeignKey("products.products.guid")),
    schema=SCHEMA,
)


class Product(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    sku: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    image_url: Mapped[typing.Optional[str]] = mapped_column(String(256), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    base_price: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    discount: Mapped[Integer] = mapped_column(Integer, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(32), nullable=False)
    tags: Mapped[typing.List[Tag]] = relationship(secondary=products_tags)
    category_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.categories.guid")
    )
    category: Mapped[Category] = relationship()
    brand_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.brands.guid"))
    brand: Mapped[Brand] = relationship()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(sku, removed_at, name="unique_product_sku")
    UniqueConstraint(name, removed_at, name="unique_product_name")

    __tablename__ = "products"
    __table_args__ = {"schema": SCHEMA}

    def __init__(
        self,
        sku: str,
        name: str,
        description: str,
        base_price: Decimal,
        quantity: Decimal,
        weight: int,
        color: str,
        category: Category,
        brand: Brand,
        tags: typing.List[Tag],
        created_at: datetime.datetime,
        image_url: typing.Optional[str] = None,
    ):
        self.guid: uuid.UUID = uuid.uuid4()
        self.sku: str = sku
        self.name: str = name
        self.description: str = description
        self.base_price: Decimal = base_price
        self.quantity: Decimal = quantity
        self.weight: int = weight
        self.color: str = color
        self.category: Category = category
        self.brand: Brand = brand
        self.tags: typing.List[Tag] = tags
        self.image_url: typing.Optional[str] = image_url
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at
