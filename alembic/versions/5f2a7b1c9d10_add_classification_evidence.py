"""Add minimal persisted classification evidence.

Revision ID: 5f2a7b1c9d10
Revises: 36d803feab41
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5f2a7b1c9d10"
down_revision: Union[str, Sequence[str], None] = "36d803feab41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("questions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("classification_input", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("classification_metadata", sa.JSON(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("questions", schema=None) as batch_op:
        batch_op.drop_column("classification_metadata")
        batch_op.drop_column("classification_input")
