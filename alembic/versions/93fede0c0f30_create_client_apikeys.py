"""create: client_apikeys

Revision ID: 93fede0c0f30
Revises: ead32b26e38a
Create Date: 2025-05-19 13:40:35.187327

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "93fede0c0f30"
down_revision: Union[str, None] = "ead32b26e38a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "client_apikeys",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "client_id",
            sa.String(20),
            sa.ForeignKey("clients.client_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("hashed_key", sa.String, nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            onupdate=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("client_apikeys")
