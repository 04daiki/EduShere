"""empty message

Revision ID: 524f60322216
Revises: b4a697143f13
Create Date: 2024-12-13 14:50:33.911859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524f60322216'
down_revision = 'b4a697143f13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('request_status', sa.Integer(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('point', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('point')

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_column('request_status')

    # ### end Alembic commands ###