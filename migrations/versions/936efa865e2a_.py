"""empty message

Revision ID: 936efa865e2a
Revises: 
Create Date: 2024-12-04 14:36:52.468977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '936efa865e2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=150), unique=True, nullable=False),  # email カラム追加
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('point', sa.Integer(), default=3),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username', name='uq_user_username')  # ユニーク制約に名前を追加
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
