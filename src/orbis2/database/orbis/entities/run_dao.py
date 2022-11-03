from sqlalchemy import Sequence, BigInteger, Column, VARCHAR, Text
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_relation import document_has_annotation_table
from orbis2.database.orbis.orbis_base import OrbisBase


class RunDao(OrbisBase):
    __tablename__ = 'run'

    run_id = Column(BigInteger, Sequence('run_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    description = Column(Text)
    documents = relationship(DocumentDao, secondary=document_has_annotation_table, backref='runs')
    annotations = relationship(AnnotationDao, secondary=document_has_annotation_table, backref='runs')
