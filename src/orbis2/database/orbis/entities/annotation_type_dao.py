from sqlalchemy import Column, BigInteger, Sequence, Text

from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationTypeDao(OrbisBase):
    __tablename__ = 'annotation_type'

    type_id = Column(BigInteger, Sequence('annotation_type_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
