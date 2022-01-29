"""add remaining posts columns

Revision ID: a1a160d613b8
Revises: 5e412f465c17
Create Date: 2022-01-29 08:43:48.548536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1a160d613b8'
down_revision = '5e412f465c17'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')))

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
