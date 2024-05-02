"""Add store module inbox model

Revision ID: 00aaaeffb22f
Revises: ef90cbf219af
Create Date: 2024-05-02 21:33:40.116709

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "00aaaeffb22f"
down_revision: Union[str, None] = "ef90cbf219af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA store")
    op.create_table(
        "inbox_events",
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
        schema="store",
    )


def downgrade() -> None:
    op.drop_table("inbox_events", schema="store")
    op.execute("DROP SCHEMA store")
