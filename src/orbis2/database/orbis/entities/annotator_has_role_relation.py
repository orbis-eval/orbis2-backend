from sqlalchemy import Column, ForeignKey, Table

from orbis2.database.orbis.orbis_base import OrbisBase

annotator_has_role_table = Table(
    'annotator_has_role',
    OrbisBase.metadata,
    Column('annotator_id', ForeignKey('annotator.annotator_id'), primary_key=True),
    Column('role_id', ForeignKey('role.role_id'), primary_key=True),
)
