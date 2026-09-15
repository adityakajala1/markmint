"""Add student-owned resource metadata and progress tables.

Revision ID: 7a1c2d3e4f50
Revises: 5f2a7b1c9d10
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7a1c2d3e4f50"
down_revision: Union[str, Sequence[str], None] = "5f2a7b1c9d10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    document_columns = {column["name"] for column in inspector.get_columns("documents")}
    with op.batch_alter_table("documents", schema=None) as batch_op:
        if "owner_id" not in document_columns:
            batch_op.add_column(sa.Column("owner_id", sa.String(), nullable=True))
        if "processing_status" not in document_columns:
            batch_op.add_column(sa.Column("processing_status", sa.String(), nullable=True))
        if "uploaded_at" not in document_columns:
            batch_op.add_column(sa.Column("uploaded_at", sa.DateTime(), nullable=True))
        if "owner_id" not in document_columns:
            batch_op.create_index("ix_documents_owner_id", ["owner_id"], unique=False)

    if not inspector.has_table("student_topic_progress"):
        op.create_table(
        "student_topic_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.String(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("practice_attempted", sa.Integer(), nullable=True),
        sa.Column("practice_correct", sa.Integer(), nullable=True),
        sa.Column("last_studied_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_student_topic_progress_id", "student_topic_progress", ["id"])
        op.create_index("ix_student_topic_progress_student_id", "student_topic_progress", ["student_id"])
        op.create_index("ix_student_topic_progress_topic_id", "student_topic_progress", ["topic_id"])

    if not inspector.has_table("student_resource_progress"):
        op.create_table(
        "student_resource_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.String(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("viewed", sa.Boolean(), nullable=True),
        sa.Column("last_viewed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"]),
        sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_student_resource_progress_id", "student_resource_progress", ["id"])
        op.create_index("ix_student_resource_progress_student_id", "student_resource_progress", ["student_id"])
        op.create_index("ix_student_resource_progress_document_id", "student_resource_progress", ["document_id"])


def downgrade() -> None:
    op.drop_index("ix_student_resource_progress_document_id", table_name="student_resource_progress")
    op.drop_index("ix_student_resource_progress_student_id", table_name="student_resource_progress")
    op.drop_index("ix_student_resource_progress_id", table_name="student_resource_progress")
    op.drop_table("student_resource_progress")
    op.drop_index("ix_student_topic_progress_topic_id", table_name="student_topic_progress")
    op.drop_index("ix_student_topic_progress_student_id", table_name="student_topic_progress")
    op.drop_index("ix_student_topic_progress_id", table_name="student_topic_progress")
    op.drop_table("student_topic_progress")
    with op.batch_alter_table("documents", schema=None) as batch_op:
        batch_op.drop_index("ix_documents_owner_id")
        batch_op.drop_column("uploaded_at")
        batch_op.drop_column("processing_status")
        batch_op.drop_column("owner_id")
