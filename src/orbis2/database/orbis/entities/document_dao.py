from sqlalchemy import Column, Sequence, BigInteger, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
# from orbis2.database.orbis.entities.document_has_metadata_relation import document_has_metadata_table
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentDao(OrbisBase):
    __tablename__ = 'document'

    document_id = Column(BigInteger, Sequence('document_id_seq'), primary_key=True)
    content = Column(Text, nullable=False)
    runs = relationship(RunHasDocumentDao, back_populates='document')
    data = relationship('MetadataDao', secondary='document_has_metadata', back_populates='documents')

    __table_args__ = (
        # ',' after Index(), is necessary, since the value of table_args must be a tuple, dictionary, or None
        Index(
            'document_text_idx',
            func.to_tsvector('english', content),
            postgresql_using='gin'
        ),
    )
