import typing

from pydantic import BaseModel, PositiveInt


class ProductUpdate(BaseModel):
    guid: str
    sku: str
    name_en: str
    name_pl: str
    image_url: typing.Optional[str]
    description_en: str
    description_pl: str
    base_price_usd: str
    base_price_pln: str
    discounted_price_usd: str
    discounted_price_pln: str
    quantity: PositiveInt
    weight: PositiveInt
    color_en: str
    color_pl: str
    tags_en: typing.List[str]
    tags_pl: typing.List[str]
    category_en: str
    category_pl: str
    brand_name: str
    brand_logo_url: str
