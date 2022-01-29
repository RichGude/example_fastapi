"""add content column to posts table

Revision ID: 925ddbc1ef05
Revises: 8ffed157a4da
Create Date: 2022-01-29 05:44:24.485688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '925ddbc1ef05'
down_revision = '8ffed157a4da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

def downgrade():
    op.drop_column('posts', 'content')
