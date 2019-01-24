"""Add cascade delete

Revision ID: c8735fa14a0a
Revises: 34b9bb5fa388
Create Date: 2018-09-04 13:54:40.031238
"""

from alembic import op
import sqlalchemy as sa

from anitya.db.migrations import utils


# revision identifiers, used by Alembic.
revision = 'c8735fa14a0a'
down_revision = '34b9bb5fa388'


def upgrade():
    ''' Rename column `distro` in packages table. '''
    # if utils.has_column('packages', 'distro'):
    #     try:
    #         op.alter_column(
    #             'packages',
    #             'distro',
    #             new_column_name='distro_name')
    #     except sa.exc.OperationalError:
    #         print('fixme')
    pass


def downgrade():
    pass
