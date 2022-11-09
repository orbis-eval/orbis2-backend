from sqlalchemy import Table, Column, ForeignKey

from orbis2.database.orbis.orbis_base import OrbisBase

run_derived_from_table = Table(
    'run_derived_from',
    OrbisBase.metadata,
    Column('parent_id', ForeignKey('run.run_id'), primary_key=True),
    Column('child_id', ForeignKey('run.run_id'), primary_key=True),
)
