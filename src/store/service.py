from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.time import LocalTimeProvider, TimeProvider
from src.store.dto import ProductUpdate
from src.store.model import InboxEvent, InboxEventType


class StoreService:
    def __init__(self, time_provider: TimeProvider = Depends(LocalTimeProvider)):
        self._time_provider = time_provider

    async def post_product_update_to_inbox(
        self, dto: ProductUpdate, session: AsyncSession
    ) -> None:
        event = InboxEvent(
            dto.model_dump(), InboxEventType.PRODUCT_UPDATED, self._time_provider.now()
        )
        session.add(event)
