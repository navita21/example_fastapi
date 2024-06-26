"""add age column to posts table

Revision ID: 63691f822f79
Revises: 4102a92ca130
Create Date: 2024-06-25 19:04:17.469297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63691f822f79'
down_revision: Union[str, None] = '4102a92ca130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('age', sa.Integer(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts','age')
    pass
