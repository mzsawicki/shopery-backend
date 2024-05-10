from fastapi import APIRouter, Depends, status

from src.store.dto import ProductListPage
from src.store.service import StoreService

router = APIRouter(tags=["store"])


@router.get(
    "/offer",
    response_model=ProductListPage,
    status_code=status.HTTP_200_OK,
    name="Search store offer",
)
async def get_products(
    page_number: int = 0, page_size: int = 10, service: StoreService = Depends()
):
    return await service.search_offer(page_number, page_size)
