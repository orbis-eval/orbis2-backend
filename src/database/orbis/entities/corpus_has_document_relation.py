from sqlalchemy import Column, Table, ForeignKey

from src.database.orbis.orbis_base import OrbisBase

corpus_has_document_table = Table(
    'corpus_has_document_table',
    OrbisBase.metadata,
    Column('corpus_id', ForeignKey('corpus.corpus_id'), primary_key=True),
    Column('document_id', ForeignKey('document.document_id'), primary_key=True),
)
