from sqlalchemy import Column, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.database.orbis.entities.annotation_dao import AnnotationDao
from src.database.orbis.orbis_base import OrbisBase


class MetadataDao(OrbisBase):
    __tablename__ = 'metadata'

    annotation_id = Column(BigInteger, ForeignKey('annotation.annotation_id'))
    annotation = relationship(AnnotationDao, backref='metadata')
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
