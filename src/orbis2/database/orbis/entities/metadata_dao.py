from sqlalchemy import Column, Text, Integer, Sequence
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class MetadataDao(OrbisBase):
    __tablename__ = 'metadata'

    metadata_id = Column(Integer, Sequence('metadata_id_seq'), primary_key=True)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    documents = relationship('DocumentDao', secondary='document_has_metadata', back_populates='data')
