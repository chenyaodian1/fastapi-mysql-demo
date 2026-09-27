"""Edit replace id integers in all models to use UUID instead

Revision ID: d98dd8ec85a3
Revises: 9c0a54914c78
Create Date: 2024-07-19 04:08:04.000976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd98dd8ec85a3'
down_revision = '9c0a54914c78'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new UUID column with a default UUID value (MySQL uses UUID() function)
    op.add_column('user', sa.Column('new_id', sa.CHAR(36), nullable=True))
    op.add_column('item', sa.Column('new_id', sa.CHAR(36), nullable=True))
    op.add_column('item', sa.Column('new_owner_id', sa.CHAR(36), nullable=True))

    # Populate the new columns with UUIDs
    op.execute('UPDATE `user` SET new_id = UUID()')
    op.execute('UPDATE item SET new_id = UUID()')
    op.execute('UPDATE item SET new_owner_id = (SELECT new_id FROM `user` WHERE `user`.id = item.owner_id)')

    # MySQL requires full column definition for alter_column
    # Set the new_id as not nullable
    op.alter_column('user', 'new_id', type_=sa.CHAR(36), nullable=False)
    op.alter_column('item', 'new_id', type_=sa.CHAR(36), nullable=False)

    # Drop old columns and rename new columns
    op.drop_constraint('item_ibfk_1', 'item', type_='foreignkey')
    op.drop_column('item', 'owner_id')
    # MySQL rename requires full column definition
    op.alter_column('item', 'new_owner_id', type_=sa.CHAR(36), nullable=False, new_column_name='owner_id')

    op.drop_column('user', 'id')
    op.alter_column('user', 'new_id', type_=sa.CHAR(36), nullable=False, new_column_name='id')

    op.drop_column('item', 'id')
    op.alter_column('item', 'new_id', type_=sa.CHAR(36), nullable=False, new_column_name='id')

    # Create primary key constraint
    op.create_primary_key('user_pkey', 'user', ['id'])
    op.create_primary_key('item_pkey', 'item', ['id'])

    # Recreate foreign key constraint
    op.create_foreign_key('item_owner_id_fkey', 'item', 'user', ['owner_id'], ['id'])


def downgrade():
    # Reverse the upgrade process
    op.add_column('user', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('item', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('item', sa.Column('old_owner_id', sa.Integer, nullable=True))

    # Populate the old columns - use row numbers since we can't restore original integers
    op.execute('SET @row_num = 0')
    op.execute('UPDATE `user` SET old_id = (SELECT @row_num := @row_num + 1)')
    op.execute('SET @row_num = 0')
    op.execute('UPDATE item SET old_id = (SELECT @row_num := @row_num + 1)')

    # Update owner_id references
    op.execute('UPDATE item SET old_owner_id = (SELECT id FROM `user` WHERE `user`.new_id = item.owner_id)')

    # Drop new columns and rename old columns back
    op.drop_constraint('item_owner_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'owner_id')
    op.alter_column('item', 'old_owner_id', type_=sa.Integer, nullable=True, new_column_name='owner_id')

    op.drop_column('user', 'id')
    op.alter_column('user', 'old_id', type_=sa.Integer, nullable=False, new_column_name='id')

    op.drop_column('item', 'id')
    op.alter_column('item', 'old_id', type_=sa.Integer, nullable=False, new_column_name='id')

    # Create primary key constraint
    op.create_primary_key('user_pkey', 'user', ['id'])
    op.create_primary_key('item_pkey', 'item', ['id'])

    # Recreate foreign key constraint
    op.create_foreign_key('item_owner_id_fkey', 'item', 'user', ['owner_id'], ['id'])
