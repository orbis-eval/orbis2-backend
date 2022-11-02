from sqlalchemy import Column, Integer, VARCHAR, Sequence
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.corpus_has_document_relation import corpus_has_document_table
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusDao(OrbisBase):
    __tablename__ = 'corpus'

    corpus_id = Column(Integer, Sequence('corpus_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    documents = relationship(DocumentDao, secondary=corpus_has_document_table, backref='corpora')
