from sqlalchemy import Column, Sequence, BigInteger, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.document_has_annotation_relation import document_has_annotation_table
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentDao(OrbisBase):
    __tablename__ = 'document'

    document_id = Column(BigInteger, Sequence('document_id_seq'), primary_key=True)
    content = Column(Text, nullable=False)
    annotations = relationship(AnnotationDao, secondary=document_has_annotation_table, backref='documents')

    __table_args__ = (
        # ',' after Index(), is necessary, since the value of table_args must be a tuple, dictionary, or None
        Index(
            'document_text_idx',
            func.to_tsvector('english', content),
            postgresql_using='gin'
        ),
    )
