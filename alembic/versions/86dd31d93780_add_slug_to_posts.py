"""add slug to posts

Revision ID: 86dd31d93780
Revises: 5c70e7613fd1
Create Date: 2022-03-29 08:57:54.292994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86dd31d93780'
down_revision = '5c70e7613fd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('slug', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'slug')
    # ### end Alembic commands ###
