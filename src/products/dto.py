import typing
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class NewProduct(BaseModel):
    sku: str = Field(min_length=3, max_length=16, examples=["2,51,594"])
    name: str = Field(min_length=3, max_length=64, examples=["Chinese Cabbage"])
    image_url: typing.Optional[str] = Field(
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"]
    )
    description: str = Field(
        min_length=3,
        max_length=4096,
        examples=[
            "Sed commodo aliquam dui ac porta. Fusce ipsum felis, imperdiet at posuere ac, viverra at mauris (...)"
        ],
    )
    base_price: Decimal = Field(decimal_places=2, examples=[Decimal("48.00")])
    discount: PositiveInt = Field(lt=100, examples=[64])
    quantity: Decimal = Field(ge=1, examples=[5413])
    weight: PositiveInt = Field(gt=0, examples=[3])
    color: str = Field(min_length=3, max_length=16, examples=["Green"])
    tags_guids: typing.List[uuid.UUID] = Field(
        examples=[[uuid.uuid4() for _ in range(5)]]
    )
    category_guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    brand_guid: uuid.UUID = Field(examples=[uuid.uuid4()])


class TagItem(BaseModel):
    guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    tag: str = Field(examples=["Vegetables", "Healthy", "Chinese", "Cabbage", "Green"])

    model_config = ConfigDict(from_attributes=True, frozen=True)


class CategoryItem(BaseModel):
    guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    name: str = Field(examples=["Vegetables"])

    model_config = ConfigDict(from_attributes=True, frozen=True)


class BrandItem(BaseModel):
    guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    name: str = Field(examples=["Farmary"])
    logo_url: typing.Optional[str] = Field(
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"]
    )

    model_config = ConfigDict(from_attributes=True, frozen=True)


class ProductDetail(BaseModel):
    guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    sku: str = Field(examples=["2,51,594"])
    name: str = Field(examples=["Chinese Cabbage"])
    image_url: typing.Optional[str] = Field(
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"]
    )
    description: str = Field(
        examples=[
            "Sed commodo aliquam dui ac porta. Fusce ipsum felis, imperdiet at posuere ac, viverra at mauris (...)"
        ]
    )
    base_price: Decimal = Field(examples=[Decimal("48.00")])
    discount: typing.Optional[PositiveInt] = Field(examples=[64])
    quantity: PositiveInt = Field(examples=[5413])
    weight: PositiveInt = Field(examples=[Decimal("3")])
    color: str = Field(examples=["Green"])
    tags: typing.List[TagItem]
    category: CategoryItem
    brand: BrandItem

    model_config = ConfigDict(from_attributes=True, frozen=True)


class ProductListItem(BaseModel):
    guid: uuid.UUID = Field(examples=[uuid.uuid4()])
    sku: str = Field(examples=["2,51,594"])
    name: str = Field(examples=["Chinese Cabbage"])
    image_url: typing.Optional[str] = Field(
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"]
    )

    model_config = ConfigDict(from_attributes=True, frozen=True)


class ProductList(BaseModel):
    page_number: int = Field(examples=[1])
    pages_count: int = Field(examples=[10])
    page_size: int = Field(examples=[5])
    items: typing.List[ProductListItem]

    model_config = ConfigDict(from_attributes=True, frozen=True)


class NewTag(BaseModel):
    tag: str = Field(
        min_length=3,
        max_length=16,
        examples=["Vegetables", "Healthy", "Chinese", "Cabbage", "Green"],
    )


class TagsList(BaseModel):
    page_number: int = Field(examples=[1])
    pages_count: int = Field(examples=[10])
    page_size: int = Field(examples=[5])
    items: typing.List[TagItem]


class NewCategory(BaseModel):
    name: str = Field(min_length=3, max_length=64, examples=["Vegetables"])


class CategoryList(BaseModel):
    page_number: int = Field(examples=[1])
    pages_count: int = Field(examples=[10])
    page_size: int = Field(examples=[5])
    items: typing.List[CategoryItem]


class NewBrand(BaseModel):
    name: str = Field(min_length=3, max_length=64, examples=["Farmary"])
    logo_url: typing.Optional[str] = Field(
        min_length=16,
        max_length=256,
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"],
    )


class BrandList(BaseModel):
    page_number: int = Field(examples=[1])
    pages_count: int = Field(examples=[10])
    page_size: int = Field(examples=[5])
    items: typing.List[BrandItem]
