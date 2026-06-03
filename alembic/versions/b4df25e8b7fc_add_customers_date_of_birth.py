"""add customers date_of_birth

Revision ID: b4df25e8b7fc
Revises: 8bc5cc191cdc
Create Date: 2026-05-20 17:28:21.355254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4df25e8b7fc'
down_revision: Union[str, Sequence[str], None] = '8bc5cc191cdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        ALTER TABLE customers
        ADD COLUMN date_of_birth TIMESTAMP;
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE customers
        DROP COLUMN date_of_birth;
        """
    )