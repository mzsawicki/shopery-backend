"""Add products module tables

Revision ID: 17058ede26d6
Revises: 
Create Date: 2024-04-20 16:58:26.287047

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17058ede26d6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA products")
    op.create_table(
        "brands",
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("logo_url", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
        sa.UniqueConstraint("name", "removed_at", name="unique_brand_name"),
        schema="products",
    )
    op.create_table(
        "categories",
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
        sa.UniqueConstraint("name", "removed_at", name="unique_category_name"),
        schema="products",
    )
    op.create_table(
        "tags",
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("tag", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
        sa.UniqueConstraint("tag", "removed_at", name="unique_tag"),
        schema="products",
    )
    op.create_table(
        "products",
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("sku", sa.String(length=16), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("image_url", sa.String(length=256), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("base_price", sa.NUMERIC(precision=4), nullable=False),
        sa.Column("discount", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.NUMERIC(precision=4), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column("color", sa.String(length=32), nullable=False),
        sa.Column("category_guid", sa.UUID(), nullable=False),
        sa.Column("brand_guid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["brand_guid"],
            ["products.brands.guid"],
        ),
        sa.ForeignKeyConstraint(
            ["category_guid"],
            ["products.categories.guid"],
        ),
        sa.PrimaryKeyConstraint("guid"),
        sa.UniqueConstraint("name", "removed_at", name="unique_product_name"),
        sa.UniqueConstraint("sku", "removed_at", name="unique_product_sku"),
        schema="products",
    )
    op.create_table(
        "products_tags",
        sa.Column("tag_guid", sa.UUID(), nullable=True),
        sa.Column("product_guid", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_guid"],
            ["products.products.guid"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_guid"],
            ["products.tags.guid"],
        ),
        schema="products",
    )


def downgrade() -> None:
    op.drop_table("products_tags", schema="products")
    op.drop_table("products", schema="products")
    op.drop_table("tags", schema="products")
    op.drop_table("categories", schema="products")
    op.drop_table("brands", schema="products")
    op.execute("DROP SCHEMA products")
