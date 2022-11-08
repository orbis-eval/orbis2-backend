from sqlalchemy import Column, Table, ForeignKey

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.orbis_base import OrbisBase

document_has_metadata_table = Table(
    'document_has_metadata',
    OrbisBase.metadata,
    Column('document_id', ForeignKey(DocumentDao.document_id), primary_key=True),
    Column('metadata_id', ForeignKey(MetadataDao.metadata_id), primary_key=True),
)
