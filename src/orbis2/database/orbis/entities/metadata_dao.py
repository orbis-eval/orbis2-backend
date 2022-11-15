from sqlalchemy import Column, Text, Sequence, BigInteger
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class MetadataDao(OrbisBase):
    __tablename__ = 'metadata'

    metadata_id = Column(BigInteger, Sequence('metadata_id_seq'), primary_key=True)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    documents = relationship('DocumentDao', secondary='document_has_metadata', back_populates='meta_data')
    annotations = relationship('AnnotationDao', secondary='annotation_has_metadata', back_populates='meta_data')
