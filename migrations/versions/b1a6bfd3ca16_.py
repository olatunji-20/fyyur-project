"""empty message

Revision ID: b1a6bfd3ca16
Revises: c7334e9343c1
Create Date: 2022-08-10 20:55:27.543802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1a6bfd3ca16'
down_revision = 'c7334e9343c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'website_link')
    op.drop_column('venue', 'genres')
    # ### end Alembic commands ###