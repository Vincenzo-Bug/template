"""Establish the template migration baseline.

Revision ID: 20260726_0001
Revises:
Create Date: 2026-07-26

The baseline is deliberately empty. Domain tables are created only when their
product requirements and physical schema have been approved.
"""

from collections.abc import Sequence

revision: str = "20260726_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Establish the approved migration lineage."""


def downgrade() -> None:
    """Remove the template migration lineage."""
