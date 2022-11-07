from sqlalchemy import Column, Integer, VARCHAR, Sequence
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusDao(OrbisBase):
    __tablename__ = 'corpus'

    corpus_id = Column(Integer, Sequence('corpus_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    runs = relationship('RunDao', back_populates='corpus')
