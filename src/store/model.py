import datetime
import typing
import uuid

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
