"""empty message

Revision ID: b4a697143f13
Revises: 3200e7e3a829
Create Date: 2024-12-12 10:21:29.825574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a697143f13'
down_revision = '3200e7e3a829'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient_id', sa.Integer(), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_requests_user_id_user'), 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_requests_recipient_id_user'), 'user', ['recipient_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_requests_post_id_posts'), 'posts', ['post_id'], ['post_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_requests_post_id_posts'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_requests_recipient_id_user'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_requests_user_id_user'), type_='foreignkey')
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('recipient_id')

    # ### end Alembic commands ###
