from sqlalchemy import Sequence, BigInteger, Column, VARCHAR, Text, ForeignKey
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class RunDao(OrbisBase):
    __tablename__ = 'run'

    run_id = Column(BigInteger, Sequence('run_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    description = Column(Text)
    documents = relationship('RunHasDocumentDao', back_populates='run')
    corpus_id = Column(ForeignKey('corpus.corpus_id'), nullable=False)
    corpus = relationship('CorpusDao', back_populates='runs')
