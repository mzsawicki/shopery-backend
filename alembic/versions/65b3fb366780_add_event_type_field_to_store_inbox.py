"""Add event_type field to store inbox

Revision ID: 65b3fb366780
Revises: 00aaaeffb22f
Create Date: 2024-05-03 00:34:06.558455

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65b3fb366780"
down_revision: Union[str, None] = "00aaaeffb22f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    event_type = postgresql.ENUM(
        "PRODUCT_UPDATED",
        "PRODUCT_REMOVED",
        "CATEGORY_UPDATED",
        "CATEGORY_REMOVED",
        "TAG_REMOVED",
        name="inboxeventtype",
    )
    event_type.create(op.get_bind())
    op.add_column(
        "inbox_events",
        sa.Column(
            "event_type",
            event_type,
            nullable=False,
        ),
        schema="store",
    )


def downgrade() -> None:
    op.drop_column("inbox_events", "event_type", schema="store")
    event_type = postgresql.ENUM(
        "PRODUCT_UPDATED",
        "PRODUCT_REMOVED",
        "CATEGORY_UPDATED",
        "CATEGORY_REMOVED",
        "TAG_REMOVED",
        name="inboxeventtype",
    )
    event_type.drop(op.get_bind())
