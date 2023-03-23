from sqlalchemy import Sequence, BigInteger, Column, VARCHAR, Text, ForeignKey
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.run_derived_from_relation import run_derived_from_table
from orbis2.database.orbis.orbis_base import OrbisBase


class RunDao(OrbisBase):
    __tablename__ = 'run'

    run_id = Column(BigInteger, Sequence('run_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False, unique=True)
    description = Column(Text)
    run_has_documents = relationship('RunHasDocumentDao',
                                     cascade='save-update, merge, delete, delete-orphan')
    corpus_id = Column(ForeignKey(CorpusDao.corpus_id), nullable=False)
    corpus = relationship(CorpusDao)
    parents = relationship('RunDao', secondary=run_derived_from_table,
                       primaryjoin=run_derived_from_table.c.parent_id == run_id,
                       secondaryjoin=run_derived_from_table.c.child_id == run_id)
