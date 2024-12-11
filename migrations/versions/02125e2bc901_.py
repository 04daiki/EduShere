"""empty message

Revision ID: 02125e2bc901
Revises: 
Create Date: 2024-12-10 11:43:10.249866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02125e2bc901'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('post_text', sa.String(length=200), nullable=True),
    sa.Column('timestamps', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(), nullable=False),
    sa.Column('item_name', sa.String(length=50), nullable=False),
    sa.Column('condition', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('genre', sa.Integer(), nullable=False),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('posts')
    # ### end Alembic commands ###