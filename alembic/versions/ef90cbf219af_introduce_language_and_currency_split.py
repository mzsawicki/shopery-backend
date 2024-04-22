"""Introduce language and currency split

Revision ID: ef90cbf219af
Revises: 17058ede26d6
Create Date: 2024-04-22 20:34:42.363920

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ef90cbf219af"
down_revision: Union[str, None] = "17058ede26d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column("name_en", sa.String(length=64), nullable=False),
        schema="products",
    )
    op.add_column(
        "categories",
        sa.Column("name_pl", sa.String(length=64), nullable=False),
        schema="products",
    )
    op.drop_constraint(
        "unique_category_name", "categories", schema="products", type_="unique"
    )
    op.create_unique_constraint(
        "unique_category_name_en",
        "categories",
        ["name_en", "removed_at"],
        schema="products",
    )
    op.create_unique_constraint(
        "unique_category_name_pl",
        "categories",
        ["name_pl", "removed_at"],
        schema="products",
    )
    op.drop_column("categories", "name", schema="products")
    op.add_column(
        "products",
        sa.Column("name_en", sa.String(length=64), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("name_pl", sa.String(length=64), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("description_en", sa.Text(), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("description_pl", sa.Text(), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("base_price_usd", sa.NUMERIC(precision=4), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("base_price_pln", sa.NUMERIC(precision=4), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("color_en", sa.String(length=32), nullable=False),
        schema="products",
    )
    op.add_column(
        "products",
        sa.Column("color_pl", sa.String(length=32), nullable=False),
        schema="products",
    )
    op.drop_constraint(
        "unique_product_name", "products", schema="products", type_="unique"
    )
    op.create_unique_constraint(
        "unique_product_name_en",
        "products",
        ["name_en", "removed_at"],
        schema="products",
    )
    op.create_unique_constraint(
        "unique_product_name_pl",
        "products",
        ["name_pl", "removed_at"],
        schema="products",
    )
    op.drop_column("products", "base_price", schema="products")
    op.drop_column("products", "name", schema="products")
    op.drop_column("products", "description", schema="products")
    op.drop_column("products", "color", schema="products")
    op.add_column(
        "tags", sa.Column("pl", sa.String(length=16), nullable=False), schema="products"
    )
    op.add_column(
        "tags", sa.Column("en", sa.String(length=16), nullable=False), schema="products"
    )
    op.drop_constraint("unique_tag", "tags", schema="products", type_="unique")
    op.create_unique_constraint(
        "unique_tag_en", "tags", ["en", "removed_at"], schema="products"
    )
    op.create_unique_constraint(
        "unique_tag_pl", "tags", ["pl", "removed_at"], schema="products"
    )
    op.drop_column("tags", "tag", schema="products")


def downgrade() -> None:
    op.add_column(
        "tags",
        sa.Column("tag", sa.VARCHAR(length=16), autoincrement=False, nullable=True),
        schema="products",
    )
    op.execute("UPDATE products.tags SET tag = 'missing_tag'")
    op.alter_column("tags", "tag", nullable=False, schema="products")

    op.drop_constraint("unique_tag_pl", "tags", schema="products", type_="unique")
    op.drop_constraint("unique_tag_en", "tags", schema="products", type_="unique")
    op.create_unique_constraint(
        "unique_tag", "tags", ["tag", "removed_at"], schema="products"
    )
    op.drop_column("tags", "en", schema="products")
    op.drop_column("tags", "pl", schema="products")

    op.add_column(
        "products",
        sa.Column("color", sa.VARCHAR(length=32), autoincrement=False, nullable=True),
        schema="products",
    )
    op.execute("UPDATE products.products SET color = 'Missing'")
    op.alter_column("products", "color", nullable=False, schema="products")

    op.add_column(
        "products",
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        schema="products",
    )
    op.execute("UPDATE products.products SET description = 'Missing'")
    op.alter_column("products", "description", nullable=False, schema="products")

    op.add_column(
        "products",
        sa.Column("name", sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        schema="products",
    )
    op.execute("UPDATE products.products SET name = 'Missing'")
    op.alter_column("products", "name", nullable=False, schema="products")

    op.add_column(
        "products",
        sa.Column(
            "base_price",
            sa.NUMERIC(precision=4, scale=0),
            autoincrement=False,
            nullable=True,
        ),
        schema="products",
    )
    op.execute("UPDATE products.products SET base_price = '0'")
    op.alter_column("products", "base_price", nullable=False, schema="products")

    op.drop_constraint(
        "unique_product_name_pl", "products", schema="products", type_="unique"
    )
    op.drop_constraint(
        "unique_product_name_en", "products", schema="products", type_="unique"
    )
    op.create_unique_constraint(
        "unique_product_name", "products", ["name", "removed_at"], schema="products"
    )
    op.drop_column("products", "color_pl", schema="products")
    op.drop_column("products", "color_en", schema="products")
    op.drop_column("products", "base_price_pln", schema="products")
    op.drop_column("products", "base_price_usd", schema="products")
    op.drop_column("products", "description_pl", schema="products")
    op.drop_column("products", "description_en", schema="products")
    op.drop_column("products", "name_pl", schema="products")
    op.drop_column("products", "name_en", schema="products")

    op.add_column(
        "categories",
        sa.Column("name", sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        schema="products",
    )
    op.execute("UPDATE products.categories SET name = 'Missing'")
    op.alter_column("categories", "name", nullable=False, schema="products")

    op.drop_constraint(
        "unique_category_name_pl", "categories", schema="products", type_="unique"
    )
    op.drop_constraint(
        "unique_category_name_en", "categories", schema="products", type_="unique"
    )
    op.create_unique_constraint(
        "unique_category_name", "categories", ["name", "removed_at"], schema="products"
    )
    op.drop_column("categories", "name_pl", schema="products")
    op.drop_column("categories", "name_en", schema="products")
