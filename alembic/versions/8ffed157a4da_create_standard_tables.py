"""Create standard tables

Revision ID: 8ffed157a4da
Revises: 
Create Date: 2022-01-29 05:01:02.985524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ffed157a4da'
down_revision = None
branch_labels = None
depends_on = None

# Define functions for rolling out and rolling back revision changes
def upgrade():
    # Create a table
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))

def downgrade():
    op.drop_table('posts')
