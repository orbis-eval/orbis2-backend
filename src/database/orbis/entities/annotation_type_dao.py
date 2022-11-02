from sqlalchemy import Column, BigInteger, Sequence, Text

from src.database.orbis.orbis_base import OrbisBase


class AnnotationTypeDao(OrbisBase):
    __tablename__ = 'annotationtype'

    type_id = Column(BigInteger, Sequence('annotationtype_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
    
