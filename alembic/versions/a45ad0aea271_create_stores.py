"""create: stores

Revision ID: a45ad0aea271
Revises: 93fede0c0f30
Create Date: 2025-05-19 14:21:38.578887

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a45ad0aea271"
down_revision: Union[str, None] = "ead32b26e38a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stores",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "client_id",
            sa.Integer,
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column(
            "auth_keys",
            sa.JSON(none_as_null=True),
            nullable=False,
            comment="Credentials",
        ),
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
    op.drop_table("stores")
