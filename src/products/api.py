import uuid

from fastapi import APIRouter, Depends, Response, UploadFile, status
from fastapi.responses import JSONResponse

from src.products.dto import (BrandItem, BrandList, BrandWrite, CategoryItem,
                              CategoryList, CategoryWrite, NewTag,
                              ProductDetail, ProductList, ProductWrite,
                              TagItem, TagsList)
from src.products.service import ProductService

router = APIRouter(tags=["product management"])


@router.get(
    "/products",
    response_model=ProductList,
    status_code=status.HTTP_200_OK,
    name="Get product list",
)
async def get_products(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_product_list(page_number, page_size)


@router.get(
    "/products/{guid}",
    response_model=ProductDetail,
    status_code=status.HTTP_200_OK,
    name="Get product details",
)
async def get_product_detail(guid: uuid.UUID, service: ProductService = Depends()):
    return await service.get_product_details(guid)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductDetail,
    name="Create new product",
)
async def post_product(dto: ProductWrite, service: ProductService = Depends()):
    result = await service.add_product(dto)
    if result.success:
        return result.product
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.put(
    "/products/{guid}",
    status_code=status.HTTP_200_OK,
    name="Update product details",
)
async def put_product(
    guid: uuid.UUID, dto: ProductWrite, service: ProductService = Depends()
):
    result = await service.update_product(guid, dto)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete(
    "/products/{guid}", status_code=status.HTTP_204_NO_CONTENT, name="Remove product"
)
async def delete_product(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_product(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get(
    "/categories",
    response_model=CategoryList,
    status_code=status.HTTP_200_OK,
    name="List all categories",
)
async def get_categories(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_category_list(page_number, page_size)


@router.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryItem,
    name="Create a new category",
)
async def post_category(dto: CategoryWrite, service: ProductService = Depends()):
    result = await service.add_category(dto)
    if result.success:
        return result.category
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.put(
    "/categories/{guid}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryItem,
    name="Update a category",
)
async def put_category(
    guid: uuid.UUID, dto: CategoryWrite, service: ProductService = Depends()
):
    result = await service.update_category(guid, dto)
    if result.success:
        return result.category
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete(
    "/categories/{guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Remove a category",
)
async def delete_category(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_category(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get(
    "/brands",
    status_code=status.HTTP_200_OK,
    response_model=BrandList,
    name="List all brands",
)
async def get_brands(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_brands_list(page_number, page_size)


@router.post(
    "/brands",
    status_code=status.HTTP_201_CREATED,
    response_model=BrandItem,
    name="Create a new brand",
)
async def post_brand(dto: BrandWrite, service: ProductService = Depends()):
    result = await service.add_brand(dto)
    if result.success:
        return result.brand
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.put(
    "/brands/{guid}",
    status_code=status.HTTP_200_OK,
    response_model=BrandItem,
    name="Update a brand",
)
async def put_brand(
    guid: uuid.UUID, dto: BrandWrite, service: ProductService = Depends()
):
    result = await service.update_brand(guid, dto)
    if result.success:
        return result.brand
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete(
    "/brands/{guid}", status_code=status.HTTP_204_NO_CONTENT, name="Remove a brand"
)
async def delete_brand(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_brand(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.get(
    "/tags",
    status_code=status.HTTP_200_OK,
    response_model=TagsList,
    name="List all tags",
)
async def get_tags(
    page_number: int = 0, page_size: int = 10, service: ProductService = Depends()
):
    return await service.get_tags_list(page_number, page_size)


@router.post(
    "/tags",
    status_code=status.HTTP_201_CREATED,
    response_model=TagItem,
    name="Create a new tag",
)
async def post_tag(dto: NewTag, service: ProductService = Depends()):
    result = await service.add_tag(dto)
    if result.success:
        return result.tag
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.delete(
    "/tags/{guid}", status_code=status.HTTP_204_NO_CONTENT, name="Remove a tag"
)
async def delete_tag(guid: uuid.UUID, service: ProductService = Depends()):
    result = await service.remove_tag(guid)
    if result.success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": result.info}
        )


@router.post(
    "/product-images", status_code=status.HTTP_201_CREATED, name="Upload product image"
)
async def post_product_image(file: UploadFile, service: ProductService = Depends()):
    result = service.upload_product_image(file.file)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post(
    "/brand-logos", status_code=status.HTTP_201_CREATED, name="Upload brand logo"
)
async def post_brand_logo(file: UploadFile, service: ProductService = Depends()):
    result = service.upload_brand_logo(file.file)
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
