from sqlalchemy import Column, VARCHAR, Sequence, BigInteger
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.corpus_supports_annotation_type_relation import \
    corpus_supports_annotation_type_table
from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusDao(OrbisBase):
    __tablename__ = 'corpus'

    corpus_id = Column(BigInteger, Sequence('corpus_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    runs = relationship('RunDao', back_populates='corpus')
    supported_annotation_types = relationship('AnnotationTypeDao', secondary=corpus_supports_annotation_type_table)
