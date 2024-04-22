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
    name_en: Mapped[str] = mapped_column(String(64), nullable=False)
    name_pl: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(name_en, removed_at, name="unique_category_name_en")
    UniqueConstraint(name_pl, removed_at, name="unique_category_name_pl")

    __tablename__ = "categories"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, name_en: str, name_pl, created_at: datetime.datetime):
        self.guid: uuid.UUID = uuid.uuid4()
        self.name_en: str = name_en
        self.name_pl: str = name_pl
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at


class Tag(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    pl: Mapped[str] = mapped_column(String(16), nullable=False)
    en: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    removed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    UniqueConstraint(pl, removed_at, name="unique_tag_pl")
    UniqueConstraint(en, removed_at, name="unique_tag_en")

    __tablename__ = "tags"
    __table_args__ = {"schema": SCHEMA}

    def __init__(self, en: str, pl: str, created_at: datetime.datetime):
        self.guid: uuid.UUID = uuid.uuid4()
        self.en: str = en
        self.pl: str = pl
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
    name_en: Mapped[str] = mapped_column(String(64), nullable=False)
    name_pl: Mapped[str] = mapped_column(String(64), nullable=False)
    image_url: Mapped[typing.Optional[str]] = mapped_column(String(256), nullable=True)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_pl: Mapped[str] = mapped_column(Text, nullable=False)
    base_price_usd: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    base_price_pln: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    discount: Mapped[typing.Optional[int]] = mapped_column(Integer, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(
        postgresql.NUMERIC(AMOUNT_NUMERIC_PRECISION), nullable=False
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    color_en: Mapped[str] = mapped_column(String(32), nullable=False)
    color_pl: Mapped[str] = mapped_column(String(32), nullable=False)
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
    UniqueConstraint(name_en, removed_at, name="unique_product_name_en")
    UniqueConstraint(name_pl, removed_at, name="unique_product_name_pl")

    __tablename__ = "products"
    __table_args__ = {"schema": SCHEMA}

    def __init__(
        self,
        sku: str,
        name_en: str,
        name_pl: str,
        description_en: str,
        description_pl: str,
        base_price_usd: Decimal,
        base_price_pln: Decimal,
        quantity: Decimal,
        weight: int,
        color_en: str,
        color_pl: str,
        category: Category,
        brand: Brand,
        tags: typing.List[Tag],
        created_at: datetime.datetime,
        discount: typing.Optional[int] = None,
        image_url: typing.Optional[str] = None,
    ):
        self.guid: uuid.UUID = uuid.uuid4()
        self.sku: str = sku
        self.name_en: str = name_en
        self.name_pl: str = name_pl
        self.description_en: str = description_en
        self.description_pl: str = description_pl
        self.base_price_usd: Decimal = base_price_usd
        self.base_price_pln: Decimal = base_price_pln
        self.discount: typing.Optional[int] = discount
        self.quantity: Decimal = quantity
        self.weight: int = weight
        self.color_en: str = color_en
        self.color_pl: str = color_pl
        self.category: Category = category
        self.brand: Brand = brand
        self.tags: typing.List[Tag] = tags
        self.image_url: typing.Optional[str] = image_url
        self.created_at: datetime.datetime = created_at
        self.updated_at: datetime.datetime = created_at
