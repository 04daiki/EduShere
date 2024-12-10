"""empty message

Revision ID: a5081cfdbce0
Revises: feaf80dda4f1
Create Date: 2024-12-09 13:45:49.729111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5081cfdbce0'
down_revision = 'feaf80dda4f1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=150), nullable=False))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=150),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.create_unique_constraint('uq_user_email', ['email'])  # 名前を追加
        batch_op.drop_column('point')

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('point', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('uq_user_email', type_='unique')  # 名前を指定
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
        batch_op.drop_column('email')
