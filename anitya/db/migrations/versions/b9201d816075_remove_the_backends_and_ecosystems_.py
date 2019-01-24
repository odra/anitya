# -*- coding: utf-8 -*-
"""Remove the backends and ecosystems tables

Revision ID: b9201d816075
Revises: 9c29da0af3af
Create Date: 2017-03-22 18:46:06.281100

"""

from alembic import op
import sqlalchemy as sa

from anitya.lib import plugins
from anitya.db.migrations import utils

# revision identifiers, used by Alembic.
revision = 'b9201d816075'
down_revision = '9c29da0af3af'


def upgrade():
    """Drop the Backends and Ecosystems tables and remove foreign keys."""
    # try:
    #     op.drop_constraint(u'projects_backend_fkey', 'projects', type_='foreignkey')
    #     op.drop_constraint(u'FK_ECOSYSTEM_FOR_PROJECT', 'projects', type_='foreignkey')
    # except NotImplementedError:
    #     print('Alter not supported')
    # if not utils.has_index('projects', 'ix_projects_ecosystem_name'):
    #     op.create_index(
    #         op.f('ix_projects_ecosystem_name'), 'projects', ['ecosystem_name'], unique=False)
    # for table in ['ecosystems', 'backends']:
    #     if utils.has_table(table):
    #         op.drop_table(table)
    pass


def downgrade():
    """Restore the Backends and Ecosystems tables."""
    op.drop_index(op.f('ix_projects_ecosystem_name'), table_name='projects')
    op.create_table(
        'backends',
        sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('name', name=u'backends_pkey'),
        postgresql_ignore_search_path=False
    )
    # We have to populate the backends table before we can add the ecosystems
    # table with its foreign key constraint.
    for backend in plugins.BACKEND_PLUGINS.get_plugins():
        op.execute("INSERT INTO backends (name) VALUES ('{}');".format(backend.name))

    op.create_table(
        'ecosystems',
        sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
        sa.Column(
            'default_backend_name',
            sa.VARCHAR(length=200),
            autoincrement=False,
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ['default_backend_name'],
            [u'backends.name'],
            name=u'ecosystems_default_backend_name_fkey',
            onupdate=u'CASCADE',
            ondelete=u'CASCADE'
        ),
        sa.PrimaryKeyConstraint('name', name=u'ecosystems_pkey'),
        sa.UniqueConstraint('default_backend_name', name=u'ecosystems_default_backend_name_key')
    )
    for ecosystem in plugins.ECOSYSTEM_PLUGINS.get_plugins():
        op.execute("""
            INSERT INTO ecosystems (name, default_backend_name)
            VALUES ('{name}', '{default}');""".format(
                name=ecosystem.name, default=ecosystem.default_backend))

    op.create_foreign_key(
        u'FK_ECOSYSTEM_FOR_PROJECT',
        'projects',
        'ecosystems',
        ['ecosystem_name'],
        ['name'],
        onupdate=u'CASCADE',
        ondelete=u'SET NULL'
    )
    op.create_foreign_key(
        u'projects_backend_fkey',
        'projects', 'backends',
        ['backend'],
        ['name'],
        onupdate=u'CASCADE',
        ondelete=u'CASCADE'
    )
