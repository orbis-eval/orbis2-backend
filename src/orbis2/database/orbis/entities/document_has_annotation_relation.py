from datetime import datetime
from sqlalchemy import Table, ForeignKey, Column, TIMESTAMP

from orbis2.database.orbis.orbis_base import OrbisBase

document_has_annotation_table = Table(
    'document_has_annotation_table',
    OrbisBase.metadata,
    Column('document_id', ForeignKey('document.document_id'), primary_key=True),
    Column('annotation_id', ForeignKey('annotation.annotation_id'), primary_key=True),
    Column('run_id', ForeignKey('run.run_id'), primary_key=True),
    Column('timestamp', TIMESTAMP, default=datetime.utcnow)
)
