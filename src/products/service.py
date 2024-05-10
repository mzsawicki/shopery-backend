import math
import typing
import uuid
from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import joinedload

from src.common.config import Config
from src.common.s3 import ObjectStorageGateway, UploadResult
from src.common.sql import get_db
from src.common.time import LocalTimeProvider, TimeProvider
from src.products.dto import (BrandItem, BrandList, BrandWrite, CategoryItem,
                              CategoryList, CategoryWrite, NewTag,
                              ProductDetail, ProductList, ProductListItem,
                              ProductWrite, TagItem, TagsList)
from src.products.model import Brand, Category, Product, Tag
from src.store.dto import ProductUpdate
from src.store.service import StoreService


@dataclass(init=True, frozen=True)
class Result:
    success: bool
    info: typing.Optional[str] = None


@dataclass(init=True, frozen=True)
class ProductWriteResult:
    success: bool
    product: typing.Optional[ProductDetail] = None
    info: typing.Optional[str] = None


@dataclass(init=True, frozen=True)
class CategoryWriteResult:
    success: bool
    category: typing.Optional[CategoryItem] = None
    info: typing.Optional[str] = None


@dataclass(init=True, frozen=True)
class BrandWriteResult:
    success: bool
    brand: typing.Optional[BrandItem] = None
    info: typing.Optional[str] = None


@dataclass(init=True, frozen=True)
class TagWriteResult:
    success: bool
    tag: typing.Optional[TagItem] = None
    info: typing.Optional[str] = None


class ProductService:
    def __init__(
        self,
        store_service: StoreService = Depends(),
        session_factory: async_sessionmaker = Depends(get_db),
        s3_gateway: ObjectStorageGateway = Depends(ObjectStorageGateway),
        time_provider: TimeProvider = Depends(LocalTimeProvider),
    ):
        self._store_service = store_service
        self._session_factory = session_factory
        self._s3_gateway = s3_gateway
        self._time_provider = time_provider
        self._config = Config()

    async def add_product(self, dto: ProductWrite) -> ProductWriteResult:
        created_at = self._time_provider.now()
        async with self._session_factory(expire_on_commit=False) as session:
            does_product_exist = await _does_product_already_exist(
                dto.sku, dto.name_en, dto.name_pl, session
            )
            if does_product_exist:
                return ProductWriteResult(
                    success=False, info="Product of such sku or name already exists"
                )

            tags = await _get_tags_by_guids(dto.tags_guids, session)
            if len(tags) < len(dto.tags_guids):
                return ProductWriteResult(
                    success=False, info="Not all requested tags were found"
                )

            category = await _get_category_or_none_by_guid(dto.category_guid, session)
            if not category:
                return ProductWriteResult(
                    success=False, info=f"Category {dto.category_guid} not found"
                )

            brand = await _get_brand_or_none_by_guid(dto.brand_guid, session)
            if not brand:
                return ProductWriteResult(
                    success=False, info=f"Brand {dto.brand_guid} not found"
                )

            product = Product(
                **dto.model_dump(exclude={"tags_guids", "category_guid", "brand_guid"}),
                tags=tags,
                category=category,
                brand=brand,
                created_at=created_at,
            )
            session.add(product)

            event_guid = await self._post_product_update_to_store_inbox(
                product, session
            )

            await session.commit()

            await self._store_service.schedule_product_update(event_guid)
        return ProductWriteResult(
            product=ProductDetail.model_validate(product), success=True
        )

    async def update_product(
        self, guid: uuid.UUID, dto: ProductWrite
    ) -> ProductWriteResult:
        updated_at = self._time_provider.now()
        stmt = (
            select(Product)
            .where(Product.guid == guid)
            .where(Product.removed_at.is_(None))
            .options(
                joinedload(Product.category),
                joinedload(Product.brand),
                joinedload(Product.tags),
            )
        )
        async with self._session_factory(expire_on_commit=False) as session:
            result = await session.execute(stmt)
            product = result.unique().scalar_one_or_none()
            if not product:
                return ProductWriteResult(
                    success=False, info=f"Product {guid} not found"
                )
            tags = await _get_tags_by_guids(dto.tags_guids, session)
            if len(tags) < len(dto.tags_guids):
                return ProductWriteResult(
                    success=False, info="Not all requested tags were found"
                )
            category = await _get_category_or_none_by_guid(dto.category_guid, session)
            if not category:
                return ProductWriteResult(
                    success=False, info=f"Category {dto.category_guid} not found"
                )
            brand = await _get_brand_or_none_by_guid(dto.brand_guid, session)
            if not brand:
                return ProductWriteResult(
                    success=False, info=f"Brand {dto.brand_guid} not found"
                )
            product.sku = dto.sku
            product.name_en = dto.name_en
            product.name_pl = dto.name_pl
            product.image_url = dto.image_url
            product.description_en = dto.description_en
            product.description_pl = dto.description_pl
            product.base_price_usd = dto.base_price_usd
            product.base_price_pln = dto.base_price_pln
            product.discount = dto.discount
            product.quantity = dto.quantity
            product.weight = dto.weight
            product.color_en = dto.color_en
            product.color_pl = dto.color_pl
            product.tags = tags
            product.category = category
            product.brand = brand
            product.updated_at = updated_at
            session.add(product)

            event_guid = await self._post_product_update_to_store_inbox(
                product, session
            )

            await session.commit()

            await self._store_service.schedule_product_update(event_guid)
        return ProductWriteResult(
            success=True, product=ProductDetail.model_validate(product)
        )

    async def get_product_list(self, page_number: int, page_size: int) -> ProductList:
        products_stmt = (
            select(Product)
            .where(Product.removed_at.is_(None))
            .limit(page_size)
            .offset(page_number * page_size)
        )

        count_stmt = select(func.count()).select_from(
            select(Product).where(Product.removed_at.is_(None)).subquery()
        )
        async with self._session_factory() as session:
            products_result = await session.execute(products_stmt)

            count_result = await session.execute(count_stmt)

        products = products_result.unique().scalars().all()
        all_products_count = count_result.scalar_one()
        pages_count = math.ceil(all_products_count / page_size)

        return ProductList(
            page_number=page_number,
            pages_count=pages_count,
            page_size=page_size,
            items=[ProductListItem.model_validate(product) for product in products],
        )

    async def get_product_details(
        self, guid: uuid.UUID
    ) -> typing.Optional[ProductDetail]:
        stmt = (
            select(Product)
            .where(Product.guid == guid)
            .where(Product.removed_at.is_(None))
            .options(
                joinedload(Product.category),
                joinedload(Product.brand),
                joinedload(Product.tags),
            )
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
        product = result.unique().scalar_one_or_none()
        if product:
            assert product
            return ProductDetail.model_validate(product)
        else:
            return None

    async def remove_product(self, guid: uuid.UUID) -> Result:
        removed_at = self._time_provider.now()
        stmt = (
            select(Product)
            .where(Product.guid == guid)
            .where(Product.removed_at.is_(None))
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            product = result.unique().scalar_one_or_none()
            if not product:
                return Result(success=False, info=f"Product {guid} not found")
            product.removed_at = removed_at
            session.add(product)

            event_guid = await self._store_service.post_product_removal_to_inbox(
                product.guid, session
            )
            await session.commit()

            await self._store_service.schedule_product_removal(event_guid)
        return Result(success=True)

    async def add_category(self, dto: CategoryWrite) -> CategoryWriteResult:
        created_at = self._time_provider.now()
        category = Category(dto.name_en, dto.name_pl, created_at)
        async with self._session_factory(expire_on_commit=False) as session:
            category_already_exists = await _does_category_already_exist(
                dto.name_en, dto.name_pl, session
            )
            if category_already_exists:
                return CategoryWriteResult(
                    success=False,
                    info=f"Category {dto.name_en}/{dto.name_pl} already exists",
                )
            session.add(category)
            await session.commit()
        return CategoryWriteResult(
            success=True, category=CategoryItem.model_validate(category)
        )

    async def update_category(
        self, guid: uuid.UUID, dto: CategoryWrite
    ) -> CategoryWriteResult:
        updated_at = self._time_provider.now()
        stmt = (
            select(Category)
            .where(Category.guid == guid)
            .where(Category.removed_at.is_(None))
        )
        async with self._session_factory(expire_on_commit=False) as session:
            result = await session.execute(stmt)
            category = result.unique().scalar_one_or_none()
            if not category:
                return CategoryWriteResult(
                    success=False, info=f"Category {guid} not found"
                )
            category.name_en = dto.name_en
            category.name_pl = dto.name_pl
            category.updated_at = updated_at
            session.add(category)
            await session.commit()
        return CategoryWriteResult(
            success=True, category=CategoryItem.model_validate(category)
        )

    async def get_category_list(self, page_number: int, page_size: int) -> CategoryList:
        categories_stmt = (
            select(Category)
            .where(Category.removed_at.is_(None))
            .limit(page_size)
            .offset(page_number * page_size)
        )

        count_stmt = select(func.count()).select_from(
            select(Category).where(Category.removed_at.is_(None)).subquery()
        )

        async with self._session_factory() as session:
            categories_result = await session.execute(categories_stmt)
            count_result = await session.execute(count_stmt)

        categories = categories_result.unique().scalars().all()
        all_categories_count = count_result.unique().scalar_one()
        pages_count = math.ceil(all_categories_count / page_size)
        return CategoryList(
            page_number=page_number,
            page_size=page_size,
            pages_count=pages_count,
            items=[CategoryItem.model_validate(category) for category in categories],
        )

    async def remove_category(self, guid: uuid.UUID) -> Result:
        removed_at = self._time_provider.now()
        products_stmt = select(
            select(Product)
            .where(Product.category_guid == guid)
            .where(Product.removed_at.is_(None))
            .exists()
        )
        category_stmt = (
            select(Category)
            .where(Category.guid == guid)
            .where(Category.removed_at.is_(None))
        )
        async with self._session_factory() as session:
            products_result = await session.execute(products_stmt)
            products_exist = products_result.unique().scalar_one()
            if products_exist:
                return Result(
                    success=False,
                    info=f"Cannot remove category having existing products",
                )
            category_result = await session.execute(category_stmt)
            category = category_result.unique().scalar_one_or_none()
            if not category:
                return Result(success=False, info=f"Category {guid} not found")
            category.removed_at = removed_at
            session.add(category)
            await session.commit()
        return Result(success=True)

    async def get_brands_list(self, page_number: int, page_size: int) -> BrandList:
        brands_stmt = (
            select(Brand)
            .where(Brand.removed_at.is_(None))
            .limit(page_size)
            .offset(page_size * page_number)
        )
        count_stmt = select(func.count()).select_from(
            select(Brand).where(Brand.removed_at.is_(None)).subquery()
        )
        async with self._session_factory() as session:
            brands_result = await session.execute(brands_stmt)
            count_result = await session.execute(count_stmt)

        brands = brands_result.unique().scalars().all()
        all_brands_count = count_result.unique().scalar_one()
        pages_count = math.ceil(all_brands_count / page_size)
        return BrandList(
            page_number=page_number,
            page_size=page_size,
            pages_count=pages_count,
            items=[BrandItem.model_validate(brand) for brand in brands],
        )

    async def add_brand(self, dto: BrandWrite) -> BrandWriteResult:
        created_at = self._time_provider.now()
        brand = Brand(dto.name, dto.logo_url, created_at)
        async with self._session_factory(expire_on_commit=False) as session:
            already_exists = await _does_brand_already_exist(dto.name, session)
            if already_exists:
                return BrandWriteResult(
                    success=False, info=f"Brand {dto.name} already exists"
                )
            session.add(brand)
            await session.commit()
        return BrandWriteResult(success=True, brand=BrandItem.model_validate(brand))

    async def update_brand(self, guid: uuid.UUID, dto: BrandWrite) -> BrandWriteResult:
        updated_at = self._time_provider.now()
        stmt = select(Brand).where(Brand.guid == guid).where(Brand.removed_at.is_(None))
        async with self._session_factory(expire_on_commit=False) as session:
            result = await session.execute(stmt)
            brand = result.unique().scalar_one_or_none()
            if not brand:
                return BrandWriteResult(success=False, info=f"Brand {guid} not found")
            brand.name = dto.name
            brand.logo_url = dto.logo_url
            brand.updated_at = updated_at
            session.add(brand)
            await session.commit()
        return BrandWriteResult(success=True, brand=BrandItem.model_validate(brand))

    async def remove_brand(self, guid: uuid.UUID) -> Result:
        removed_at = self._time_provider.now()
        brand_stmt = (
            select(Brand).where(Brand.guid == guid).where(Brand.removed_at.is_(None))
        )
        products_stmt = select(
            select(Product)
            .where(Product.brand_guid == guid)
            .where(Product.removed_at.is_(None))
            .exists()
        )
        async with self._session_factory() as session:
            brand_result = await session.execute(brand_stmt)
            products_result = await session.execute(products_stmt)
            brand = brand_result.unique().scalar_one_or_none()
            brand_products_exist = products_result.unique().scalar_one()
            if not brand:
                return Result(success=False, info=f"Brand {guid} not found")
            if brand_products_exist:
                return Result(
                    success=False, info=f"Cannot remove brand having existing products"
                )
            brand.removed_at = removed_at
            session.add(brand)
            await session.commit()
        return Result(success=True)

    async def add_tag(self, dto: NewTag) -> TagWriteResult:
        created_at = self._time_provider.now()
        async with self._session_factory(expire_on_commit=False) as session:
            if await _does_tag_already_exist(dto.en, dto.pl, session):
                return TagWriteResult(
                    success=False, info=f"Tag {dto.en}/{dto.pl} already exists"
                )
            tag = Tag(dto.en, dto.pl, created_at)
            session.add(tag)
            await session.commit()
        return TagWriteResult(success=True, tag=TagItem.model_validate(tag))

    async def get_tags_list(self, page_number: int, page_size: int) -> TagsList:
        tags_stmt = (
            select(Tag)
            .where(Tag.removed_at.is_(None))
            .limit(page_size)
            .offset(page_size * page_number)
        )
        count_stmt = select(func.count()).select_from(
            select(Tag).where(Tag.removed_at.is_(None)).subquery()
        )
        async with self._session_factory() as session:
            tags_result = await session.execute(tags_stmt)
            count_result = await session.execute(count_stmt)

        tags = tags_result.unique().scalars().all()
        all_tags_count = count_result.unique().scalar_one()
        pages_count = math.ceil(all_tags_count / page_size)
        return TagsList(
            page_number=page_number,
            page_size=page_size,
            pages_count=pages_count,
            items=[TagItem.model_validate(tag) for tag in tags],
        )

    async def remove_tag(self, guid: uuid.UUID) -> Result:
        removed_at = self._time_provider.now()
        tag_stmt = select(Tag).where(Tag.guid == guid).where(Tag.removed_at.is_(None))
        associations_stmt = select(
            select(Product).where(Product.tags.any(Tag.guid == guid)).exists()
        )
        async with self._session_factory() as session:
            tag_result = await session.execute(tag_stmt)
            associations_result = await session.execute(associations_stmt)
            tag = tag_result.unique().scalar_one_or_none()
            tagged_products_exist = associations_result.unique().scalar_one()
            if not tag:
                return Result(success=False, info=f"Brand {guid} not found")
            if tagged_products_exist:
                return Result(
                    success=False, info=f"Cannot remove tag having existing products"
                )
            tag.removed_at = removed_at
            session.add(tag)
            await session.commit()
        return Result(success=True)

    def upload_product_image(self, name: str, file: typing.BinaryIO) -> UploadResult:
        file_extension = _get_file_extension(name)
        if not _is_file_extension_valid(file_extension):
            return UploadResult(success=False, file_format_valid=False)
        if not _is_file_size_valid(file, self._config.max_upload_file_size_bytes):
            return UploadResult(success=False, file_size_ok=False)
        file_key = f"{str(uuid.uuid4())}.{file_extension}"
        return self._s3_gateway.upload_file("product-images", file_key, file)

    def upload_brand_logo(self, name: str, file: typing.BinaryIO) -> UploadResult:
        file_extension = _get_file_extension(name)
        if not _is_file_extension_valid(file_extension):
            return UploadResult(success=False, file_format_valid=False)
        if not _is_file_size_valid(file, self._config.max_upload_file_size_bytes):
            return UploadResult(success=False, file_size_ok=False)
        file_key = f"{str(uuid.uuid4())}.{file_extension}"
        return self._s3_gateway.upload_file("brand-logos", file_key, file)

    async def _post_product_update_to_store_inbox(
        self, product: Product, session: AsyncSession
    ) -> uuid.UUID:
        dto = ProductUpdate(
            guid=str(product.guid),
            sku=product.sku,
            name_en=product.name_en,
            name_pl=product.name_pl,
            image_url=product.image_url,
            description_en=product.description_en,
            description_pl=product.description_pl,
            base_price_usd=str(product.base_price_usd),
            base_price_pln=str(product.base_price_pln),
            discounted_price_usd=str(
                product.base_price_usd - product.base_price_usd * product.discount
                if product.discount
                else product.base_price_usd
            ),
            discounted_price_pln=str(
                product.base_price_pln - product.base_price_pln * product.discount
                if product.discount
                else product.base_price_pln
            ),
            quantity=product.quantity,
            weight=product.weight,
            color_en=product.color_en,
            color_pl=product.color_pl,
            tags_en=[tag.en for tag in product.tags],
            tags_pl=[tag.pl for tag in product.tags],
            category_en=product.category.name_en,
            category_pl=product.category.name_pl,
            brand_name=product.brand.name,
            brand_logo_url=product.brand.logo_url,
        )
        return await self._store_service.post_product_update_to_inbox(dto, session)


async def _get_tags_by_guids(
    guids: typing.List[uuid.UUID], session: AsyncSession
) -> typing.List[Tag]:
    stmt = select(Tag).where(Tag.guid.in_(guids)).where(Tag.removed_at.is_(None))
    result = await session.execute(stmt)
    return list(result.unique().scalars().all())


async def _get_category_or_none_by_guid(
    guid: uuid.UUID, session: AsyncSession
) -> typing.Optional[Category]:
    stmt = (
        select(Category)
        .where(Category.guid == guid)
        .where(Category.removed_at.is_(None))
    )
    result = await session.execute(stmt)
    return result.unique().scalar_one_or_none()


async def _get_brand_or_none_by_guid(
    guid: uuid.UUID, session: AsyncSession
) -> typing.Optional[Brand]:
    stmt = select(Brand).where(Brand.guid == guid).where(Brand.removed_at.is_(None))
    result = await session.execute(stmt)
    return result.unique().scalar_one_or_none()


async def _does_product_already_exist(
    product_sku: str, product_name_en: str, product_name_pl: str, session: AsyncSession
) -> bool:
    stmt = select(
        select(Product)
        .where(
            or_(
                Product.sku == product_sku,
                Product.name_en == product_name_en,
                Product.name_pl == product_name_pl,
            )
        )
        .where(Product.removed_at.is_(None))
        .exists()
    )
    result = await session.execute(stmt)
    return result.scalar_one()


async def _does_category_already_exist(
    name_en: str, name_pl: str, session: AsyncSession
) -> bool:
    stmt = select(
        select(Category)
        .where(or_(Category.name_en == name_en, Category.name_pl == name_pl))
        .where(Category.removed_at.is_(None))
        .exists()
    )
    result = await session.execute(stmt)
    return result.scalar_one()


async def _does_brand_already_exist(name: str, session: AsyncSession) -> bool:
    stmt = select(
        select(Brand)
        .where(Brand.name == name)
        .where(Brand.removed_at.is_(None))
        .exists()
    )
    result = await session.execute(stmt)
    return result.scalar_one()


async def _does_tag_already_exist(en: str, pl: str, session: AsyncSession) -> bool:
    stmt = select(
        select(Tag)
        .where(or_(Tag.en == en, Tag.pl == pl))
        .where(Tag.removed_at.is_(None))
        .exists()
    )
    result = await session.execute(stmt)
    return result.scalar_one()


def _get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]


def _is_file_extension_valid(extension: str) -> bool:
    return extension.lower() in ["jpg", "jpeg", "png"]


def _is_file_size_valid(file: typing.BinaryIO, max_file_size_bytes: int) -> bool:
    total_size = 0
    for chunk in file:
        total_size += len(chunk)
        if total_size > max_file_size_bytes:
            return False
    file.seek(0)
    return True
