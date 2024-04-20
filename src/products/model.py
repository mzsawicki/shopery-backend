import datetime
from decimal import Decimal
import typing
import uuid

from sqlalchemy import DateTime, String, Integer, Table, Column, ForeignKey, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.model import Entity, AMOUNT_NUMERIC_PRECISION


SCHEMA = "products"


class Brand(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    __tablename__ = "brands"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, name: str, logo_url: str, created_at: datetime):
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

    __tablename__ = "categories"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, name: str, created_at: datetime.datetime):
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

    __tablename__ = "tags"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, tag: str, created_at: datetime.datetime):
        self.guid: uuid.UUID = uuid.uuid4()
        self.tag: str = tag
        self.created_at: datetime.datetime = created_at


products_tags = Table(
    "products_tags",
    Entity.metadata,
    Column("tag_guid", ForeignKey("tags.guid")),
    Column("product_guid", ForeignKey("products.guid")),
    schema=SCHEMA
)


class Product(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    sku: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    base_price: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    discount: Mapped[Integer] = mapped_column(Integer, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(32), nullable=False)
    tags: Mapped[typing.List[Tag]] = relationship(secondary=products_tags)
    category_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.guid"))
    category: Mapped[Category] = relationship()
    brand_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("brands.guid"))
    brand: Mapped[uuid.UUID] = relationship()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    __tablename__ = "products"
    __table_args__ = {"schema": SCHEMA}

    def __init__(
        self, sku: str, name: str, description: str,
        base_price: Decimal, quantity: Decimal, category: Category,
        brand: Brand, tags: typing.List[Tag], created_at: datetime.datetime
    ):
        self.guid: uuid.UUID = uuid.uuid4()
        self.sku: str = sku
        self.name: str = name
        self.description: str = description
        self.base_price: Decimal = base_price
        self.quantity: Decimal = quantity
        self.category: Category = category
        self.brand: Brand = brand
        self.tags: typing.List[Tag] = tags
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at
