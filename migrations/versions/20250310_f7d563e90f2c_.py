"""empty message

Revision ID: f7d563e90f2c
Revises: 
Create Date: 2025-03-10 13:17:17.832138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7d563e90f2c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('waitlist_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('utm_source', sa.String(), nullable=False),
    sa.Column('user_full_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_waitlist_items_tg_id'), 'waitlist_items', ['tg_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_waitlist_items_tg_id'), table_name='waitlist_items')
    op.drop_table('waitlist_items')
    # ### end Alembic commands ###
