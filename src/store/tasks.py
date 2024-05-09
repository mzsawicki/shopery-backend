import logging
import uuid

from redis.asyncio import Redis
from redis.commands.json.path import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from taskiq import TaskiqDepends

from src.common.redis import get_redis_client
from src.common.sql import get_db
from src.common.tasks import broker
from src.common.time import LocalTimeProvider, TimeProvider
from src.store.model import InboxEvent


@broker.task
async def consume_product_updated_event(
    event_guid: uuid.UUID,
    time_provider: TimeProvider = TaskiqDepends(LocalTimeProvider),
    redis_client: Redis = TaskiqDepends(get_redis_client),
    session_factory: async_sessionmaker = TaskiqDepends(get_db),
) -> None:
    stmt = (
        select(InboxEvent)
        .where(InboxEvent.guid == event_guid)
        .where(InboxEvent.processed_at.is_(None))
    )
    async with session_factory() as session:
        result = await session.execute(stmt)
        event = result.scalar_one_or_none()
        if not event:
            logging.error(
                f"Could not find event {event.guid}. Was it already processed?"
            )
        else:
            product_guid = event.data["guid"]
            await redis_client.json().set(
                f"product:{product_guid}", Path.root_path(), event.data
            )
            event.processed_at = time_provider.now()
            await session.commit()


@broker.task
async def consume_product_removed_event(
    event_guid: uuid.UUID,
    time_provider: TimeProvider = TaskiqDepends(LocalTimeProvider),
    redis_client: Redis = TaskiqDepends(get_redis_client),
    session_factory: async_sessionmaker = TaskiqDepends(get_db),
) -> None:
    stmt = (
        select(InboxEvent)
        .where(InboxEvent.guid == event_guid)
        .where(InboxEvent.processed_at.is_(None))
    )
    async with session_factory() as session:
        result = await session.execute(stmt)
        event = result.scalar_one_or_none()
        if not event:
            logging.error(
                f"Could not find event {event.guid}. Was it already processed?"
            )
        else:
            product_guid = event.data["guid"]
            await redis_client.json().delete(
                f"product:{product_guid}", Path.root_path()
            )
            event.processed_at = time_provider.now()
            await session.commit()
