"""Model upstream ecosystems

Revision ID: 921c612ba0da
Revises: 2925648d8cc3
Create Date: 2016-08-09 18:44:53.119461

"""

from alembic import op
import sqlalchemy as sa

from anitya.db.migrations import utils


# revision identifiers, used by Alembic.
revision = '921c612ba0da'
down_revision = '2925648d8cc3'


def upgrade():
    pass
    # if not utils.has_column('projects', 'ecosystem_name'):
    #     op.add_column(
    #         'projects', sa.Column('ecosystem_name', sa.String(length=200), nullable=True))
    # try:
    #     if not utils.has_constraint('projects', 'UNIQ_PROJECT_NAME_PER_ECOSYSTEM'):
    #         op.create_unique_constraint(
    #             'UNIQ_PROJECT_NAME_PER_ECOSYSTEM', 'projects', ['name', 'ecosystem_name'])
    #     if not utils.has_foreign_key('projects', 'FK_ECOSYSTEM_FOR_PROJECT'):
    #         op.create_foreign_key(
    #             'FK_ECOSYSTEM_FOR_PROJECT', 'projects', 'ecosystems', ['ecosystem_name'],
    #             ['name'], onupdate='cascade', ondelete='set null')
    # #except (NotImplementedError, sa.exc.ProgrammingError, sa.exc.InternalError):
    # except Exception:
    #     print('fixme')


def downgrade():
    op.drop_constraint('FK_ECOSYSTEM_FOR_PROJECT', 'projects', type_='foreignkey')
    op.drop_constraint('UNIQ_PROJECT_NAME_PER_ECOSYSTEM', 'projects', type_='unique')
    op.drop_column('projects', 'ecosystem_name')
