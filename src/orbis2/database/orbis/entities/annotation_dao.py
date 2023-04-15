from typing import List

from sqlalchemy import Column, Integer, Sequence, BigInteger, Text, ForeignKey, ARRAY, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from orbis2.database.orbis.entities.annotation_has_metadata_relation import annotation_has_metadata_table
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationDao(OrbisBase):
    __tablename__ = 'annotation'

    annotation_id: Mapped[int] = mapped_column(BigInteger, Sequence('annotation_id_seq'), primary_key=True)
    key: Mapped[str] = mapped_column(default='')
    surface_forms: Mapped[List[str]] = mapped_column(ARRAY(Text))
    start_indices: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    end_indices: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    annotation_type_id: Mapped[AnnotationTypeDao] = mapped_column(ForeignKey(AnnotationTypeDao.type_id))
    annotation_type: Mapped[AnnotationTypeDao] = relationship()
    annotator_id: Mapped[AnnotatorDao] = Column(ForeignKey(AnnotatorDao.annotator_id))
    annotator: Mapped[AnnotatorDao] = relationship()
    meta_data: Mapped[MetadataDao] = relationship(secondary=annotation_has_metadata_table)
    __table_args__ = (CheckConstraint(func.array_length(surface_forms, 1) == func.array_length(start_indices, 1)),
                      CheckConstraint(func.array_length(start_indices, 1) == func.array_length(end_indices, 1)))
