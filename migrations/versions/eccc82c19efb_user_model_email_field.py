"""user_model_email_field

Revision ID: eccc82c19efb
Revises: 0ae6d8ec7926
Create Date: 2023-09-12 11:02:40.222469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eccc82c19efb'
down_revision = '0ae6d8ec7926'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
