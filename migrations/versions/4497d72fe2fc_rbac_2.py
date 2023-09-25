"""rbac_2

Revision ID: 4497d72fe2fc
Revises: 89f7c3d8a74c
Create Date: 2023-09-25 09:20:01.419063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4497d72fe2fc'
down_revision = '89f7c3d8a74c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_novices')
    with op.batch_alter_table('novices', schema=None) as batch_op:
        batch_op.drop_constraint('fk_novices_novice_id_users', type_='foreignkey')
        batch_op.drop_column('novice_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_users_role_id_roles'), 'roles', ['role_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_users_role_id_roles'), type_='foreignkey')
        batch_op.drop_column('role_id')

    with op.batch_alter_table('novices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('novice_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_novices_novice_id_users', 'users', ['novice_id'], ['id'])

    op.create_table('_alembic_tmp_novices',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('close_ticket', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_novices_user_id_users'),
    sa.PrimaryKeyConstraint('id', name='pk_novices')
    )
    # ### end Alembic commands ###