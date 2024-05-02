import datetime
import typing
import uuid

from redis.commands.search.field import NumericField, TagField, TextField
from sqlalchemy import DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from src.common.model import Entity

SCHEMA = "store"


class InboxEvent(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    data: Mapped[typing.Dict[str, typing.Any]] = mapped_column(
        postgresql.JSONB, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    processed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    __tablename__ = "inbox_events"
    __table_args__ = {"schema": SCHEMA}


product = (
    TagField("$.guid", as_name="guid"),
    TagField("$.sku", as_name="sku"),
    TextField("$.name_en", as_name="name_en", sortable=True),
    TextField("$.name_pl", as_name="name_pl", sortable=True),
    TextField("$.image_url", as_name="image_url", no_index=True),
    TextField("$.description_en", as_name="description_en"),
    TextField("$.description_pl", as_name="description_pl"),
    NumericField("$.base_price_usd", as_name="base_price_usd"),
    NumericField("$.base_price_pln", as_name="base_price_pln"),
    NumericField("$.discounted_price_usd", as_name="discounted_price_usd", sortable=True),
    NumericField("$.discounted_price_pln", as_name="discounted_price_pln", sortable=True),
    NumericField("$.quantity", as_name="quantity"),
    NumericField("$.weight", as_name="weight", no_index=True),
    TagField("$.color_en", as_name="color_en"),
    TagField("$.color_pl", as_name="color_pl"),
    TagField("$.tags_en", as_name="tags_en", separator=","),
    TagField("$.tags_pl", as_name="tags_pl", separator=","),
    TagField("$.category_en", as_name="category_en", sortable=True),
    TagField("$.category_pl", as_name="category_pl", sortable=True),
    TagField("$.brand_name", as_name="brand_name", sortable=True),
    TextField("$.brand_logo_url", as_name="brand_logo_url", no_index=True),
)
