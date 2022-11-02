from sqlalchemy import Column, Integer, Sequence, BigInteger, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationDao(OrbisBase):
    __tablename__ = 'annotation'

    annotation_id = Column(BigInteger, Sequence('annotation_id_seq'), primary_key=True)
    key = Column(Text)
    annotation_type_id = Column(BigInteger, ForeignKey('annotationtype.type_id'), nullable=False)
    annotation_type = relationship(AnnotationTypeDao, backref='annotations')
    annotator_id = Column(Integer, ForeignKey('annotator.annotator_id'), nullable=False)
    annotator = relationship(AnnotatorDao, backref='annotations')
    surface_forms = Column(ARRAY(Text), nullable=False)
    start_indices = Column(ARRAY(Integer), nullable=False)
    end_indices = Column(ARRAY(Integer), nullable=False)
    # TODO, anf 02.11.2022: add constraint for equal array size
