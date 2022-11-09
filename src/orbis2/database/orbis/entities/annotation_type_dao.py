from sqlalchemy import Column, BigInteger, Sequence, Text
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationTypeDao(OrbisBase):
    __tablename__ = 'annotation_type'

    type_id = Column(BigInteger, Sequence('annotation_type_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
    annotations = relationship('AnnotationDao', back_populates='annotation_type')

