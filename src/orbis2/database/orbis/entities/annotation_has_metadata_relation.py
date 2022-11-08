from sqlalchemy import Column, Table, ForeignKey

from orbis2.database.orbis.orbis_base import OrbisBase

annotation_has_metadata_table = Table(
    'annotation_has_metadata',
    OrbisBase.metadata,
    Column('annotation_id', ForeignKey('annotation.annotation_id'), primary_key=True),
    Column('metadata_id', ForeignKey('metadata.metadata_id'), primary_key=True),
)
