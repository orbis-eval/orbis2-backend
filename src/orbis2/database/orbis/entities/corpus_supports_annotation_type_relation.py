from sqlalchemy import Column, Table, ForeignKey, BigInteger

from orbis2.database.orbis.orbis_base import OrbisBase

corpus_supports_annotation_type_table = Table(
    'corpus_supports_annotation_type',
    OrbisBase.metadata,
    Column('corpus_id', ForeignKey('corpus.corpus_id'), primary_key=True),
    Column('annotation_type_id', ForeignKey('annotation_type.type_id'), primary_key=True),
    Column('color_id', BigInteger)
)
