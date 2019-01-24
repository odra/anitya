from alembic import op
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection


def get_inspector(prefix='sqlalchemy.'):
    config = op.get_context().config
    section = config.get_section(config.config_ini_section)
    engine = engine_from_config(section, prefix=prefix)
    return reflection.Inspector.from_engine(engine)


def has_table(table, prefix='sqlalchemy.'):
    insp = get_inspector(prefix)
    return table in insp.get_table_names()


def has_constraint(table, name, prefix='sqlalchemy.'):
    insp = get_inspector(prefix)
    for constraint in insp.get_unique_constraints(table):
        if name == constraint['name']:
            return True
    return False

def has_foreign_key(table, name, prefix='sqlalchemy.'):
    insp = get_inspector(prefix)
    for key in insp.get_foreign_keys(table):
        if name == name['key']:
            return True
    return False


def has_column(table, column, prefix='sqlalchemy.'):
    insp = get_inspector(prefix)
    for col in insp.get_columns(table):
        if column in col['name']:
            return True
    return False


def has_index(table, index, prefix='sqlalchemy.'):
    insp = get_inspector(prefix)
    for idx in insp.get_indexes(table):
        print(idx)
        if index in idx['name']:
            return True
    return False
