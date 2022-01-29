"""auto-vote

Revision ID: 1589848ce888
Revises: a1a160d613b8
Create Date: 2022-01-29 08:55:17.939454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1589848ce888'
down_revision = 'a1a160d613b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('votes')
    # ### end Alembic commands ###
