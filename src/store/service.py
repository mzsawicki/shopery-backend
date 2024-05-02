from sqlalchemy.ext.asyncio import AsyncSession

from src.store.dto import ProductUpdate
from src.store.model import InboxEvent, InboxEventType


async def post_product_update_to_inbox(
    dto: ProductUpdate, session: AsyncSession
) -> None:
    event = InboxEvent(dto.model_dump(), InboxEventType.PRODUCT_UPDATED, dto.updated_at)
    session.add(event)
