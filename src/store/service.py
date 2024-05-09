import math
import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from redis.asyncio import Redis
from redis.commands.search.query import Query

from src.common.redis import get_redis_client
from src.common.sql import get_db
from src.common.time import LocalTimeProvider, TimeProvider
from src.store.dto import ProductUpdate, ProductListPage, ProductListItem
from src.store.model import InboxEvent, InboxEventType
from src.store.tasks import (consume_product_removed_event,
                             consume_product_updated_event)


class StoreService:
    def __init__(
        self,
        time_provider: TimeProvider = Depends(LocalTimeProvider),
        session_factory: async_sessionmaker = Depends(get_db),
        redis_client: Redis = Depends(get_redis_client)
    ):
        self._time_provider = time_provider
        self._session_factory = session_factory
        self._redis_client = redis_client

    async def search_offer(self, page_number: int, page_size: int) -> ProductListPage:
        query = Query("*").paging(page_number * page_size, page_size)
        result = await self._redis_client.ft("idx:products").search(query)
        all_results_count = result.total
        items = [ProductListItem.model_validate_json(doc.json) for doc in result.docs]
        return ProductListPage(
            page_number=page_number,
            pages_count=math.ceil(all_results_count / page_size),
            all_results_count=all_results_count,
            items=items
        )

    async def post_product_update_to_inbox(
        self, dto: ProductUpdate, session: AsyncSession
    ) -> uuid.UUID:
        event = InboxEvent(
            dto.model_dump(), InboxEventType.PRODUCT_UPDATED, self._time_provider.now()
        )
        session.add(event)
        return event.guid

    async def post_product_removal_to_inbox(
        self, product_guid: uuid.UUID, session: AsyncSession
    ) -> uuid.UUID:
        event = InboxEvent(
            {"guid": str(product_guid)},
            InboxEventType.PRODUCT_REMOVED,
            self._time_provider.now(),
        )
        session.add(event)
        return event.guid

    @staticmethod
    async def schedule_product_update(update_event_guid: uuid.UUID) -> None:
        await consume_product_updated_event.kiq(update_event_guid)

    @staticmethod
    async def schedule_product_removal(removal_event_guid: uuid.UUID) -> None:
        await consume_product_removed_event.kiq(removal_event_guid)
