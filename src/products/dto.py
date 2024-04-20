import typing
from decimal import Decimal

from pydantic import BaseModel, PositiveInt, Field


class NewProduct(BaseModel):
    sku: str = Field(min_length=3, max_length=16, examples=["2,51,594"])
    name: str = Field(min_length=3, max_length=64, examples=["Chinese Cabbage"])
    description: str = Field(
        min_length=3,
        max_length=4096,
        examples=[
            "Sed commodo aliquam dui ac porta. Fusce ipsum felis, imperdiet at posuere ac, viverra at mauris (...)"
        ]
    )
    base_price: Decimal = Field(decimal_places=2, examples=[Decimal("48.00")])
    discount: PositiveInt = Field(lt=100, examples=[64])


class NewTag:
    tag: str = Field(min_length=3, max_length=16, examples=["Vegetables", "Healthy", "Chinese", "Cabbage", "Green"])


class NewCategory:
    name: str = Field(min_length=3, max_length=64, examples=["Vegetables"])


class NewBrand:
    name: str = Field(min_length=3, max_length=64, examples=["Farmary"])
    logo_url: typing.Optional[str] = Field(
        min_length=16,
        max_length=256,
        examples=["https://s3.eu-central-1.amazonaws.com/bucket/file"]
    )