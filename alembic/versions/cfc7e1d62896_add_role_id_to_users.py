"""Add role_id to users

Revision ID: cfc7e1d62896
Revises: 
Create Date: 2025-05-03 04:58:39.207951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfc7e1d62896'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    # ### end Alembic commands ###
