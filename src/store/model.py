import datetime
import enum
import typing
import uuid

from redis.commands.search.field import NumericField, TagField, TextField
from sqlalchemy import DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from src.common.model import Entity

SCHEMA = "store"


class InboxEventType(enum.Enum):
    PRODUCT_UPDATED = "PRODUCT_UPDATED"
    PRODUCT_REMOVED = "PRODUCT_REMOVED"
    CATEGORY_UPDATED = "CATEGORY_UPDATED"
    CATEGORY_REMOVED = "CATEGORY_REMOVED"
    TAG_REMOVED = "TAG_REMOVED"


class InboxEvent(Entity):
    guid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True
    )
    event_type: Mapped[InboxEventType] = mapped_column(
        postgresql.ENUM(InboxEventType),
        nullable=False,
    )
    data: Mapped[typing.Dict[str, typing.Any]] = mapped_column(
        postgresql.JSONB, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    processed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    __tablename__ = "inbox_events"
    __table_args__ = {"schema": SCHEMA}

    def __init__(
        self,
        data: typing.Dict[str, typing.Any],
        event_type: InboxEventType,
        created_at: datetime.datetime,
    ) -> None:
        self.guid: uuid.UUID = uuid.uuid4()
        self.data: typing.Dict[str, typing.Any] = data
        self.event_type: InboxEventType = event_type
        self.created_at: datetime.datetime = created_at


product = (
    TagField("$.guid", as_name="guid"),
    TagField("$.sku", as_name="sku"),
    TextField("$.name_en", as_name="name_en"),
    TextField("$.name_pl", as_name="name_pl"),
    TextField("$.description_en", as_name="description_en"),
    TextField("$.description_pl", as_name="description_pl"),
    NumericField(
        "$.price_usd", as_name="discounted_price_usd", sortable=True, no_index=True
    ),
    NumericField(
        "$.price_pln", as_name="discounted_price_pln", sortable=True, no_index=True
    ),
    TagField("$.tags_en", as_name="tags_en", separator=","),
    TagField("$.tags_pl", as_name="tags_pl", separator=","),
    TagField("$.category_en", as_name="category_en"),
    TagField("$.category_pl", as_name="category_pl"),
)
