from sqlalchemy import Column, Integer, Sequence, BigInteger, Text, ForeignKey, ARRAY, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotation_has_metadata_relation import annotation_has_metadata_table
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationDao(OrbisBase):
    __tablename__ = 'annotation'

    annotation_id = Column(BigInteger, Sequence('annotation_id_seq'), primary_key=True)
    key = Column(Text, default='')
    surface_forms = Column(ARRAY(Text), nullable=False)
    start_indices = Column(ARRAY(Integer), nullable=False)
    end_indices = Column(ARRAY(Integer), nullable=False)
    annotation_type_id = Column(ForeignKey(AnnotationTypeDao.type_id), nullable=False)
    annotation_type = relationship(AnnotationTypeDao)
    annotator_id = Column(ForeignKey(AnnotatorDao.annotator_id), nullable=False)
    annotator = relationship(AnnotatorDao)
    meta_data = relationship(MetadataDao, secondary=annotation_has_metadata_table)
    __table_args__ = (CheckConstraint(func.array_length(surface_forms, 1) == func.array_length(start_indices, 1)),
                      CheckConstraint(func.array_length(start_indices, 1) == func.array_length(end_indices, 1)))
