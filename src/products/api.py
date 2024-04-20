import uuid

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from src.products.dto import (BrandList, CategoryList, NewBrand, NewCategory,
                              NewProduct, NewTag, ProductDetail, ProductList,
                              TagsList)
from src.products.service import ProductService

router = APIRouter(tags=["product management"])


@router.get("/products", response_model=ProductList, status_code=status.HTTP_200_OK)
async def get_products(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_product_list(page_number, page_size)


@router.get(
    "/products/{guid}", response_model=ProductDetail, status_code=status.HTTP_200_OK
)
async def get_product_detail(guid: uuid.UUID, service: ProductService = Depends()):
    return await service.get_product_details(guid)


@router.post("/products", status_code=status.HTTP_201_CREATED)
async def post_product(dto: NewProduct, service: ProductService = Depends()):
    result = await service.add_product(dto)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete("/products/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_product(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get("/categories", response_model=CategoryList, status_code=status.HTTP_200_OK)
async def get_categories(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_category_list(page_number, page_size)


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def post_category(dto: NewCategory, service: ProductService = Depends()):
    result = await service.create_category(dto)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete("/categories/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_category(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get("/brands", status_code=status.HTTP_200_OK, response_model=BrandList)
async def get_brands(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_brands_list(page_number, page_size)


@router.post("/brands", status_code=status.HTTP_201_CREATED)
async def post_brand(dto: NewBrand, service: ProductService = Depends()):
    result = await service.add_brand(dto)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete("/brands/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_brand(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get("/tags", status_code=status.HTTP_200_OK, response_model=TagsList)
async def get_tags(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_tags_list(page_number, page_size)


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def post_tag(dto: NewTag, service: ProductService = Depends()):
    result = await service.add_tag(dto)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete("/tags/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_tag(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )
