from sqlalchemy import Column, Table, ForeignKey

from orbis2.database.orbis.orbis_base import OrbisBase

document_has_metadata_table = Table(
    'document_has_metadata',
    OrbisBase.metadata,
    Column('document_id', ForeignKey('document.document_id'), primary_key=True),
    Column('metadata_id', ForeignKey('metadata.metadata_id'), primary_key=True),
)
