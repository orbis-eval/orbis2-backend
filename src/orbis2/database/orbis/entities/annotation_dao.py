from sqlalchemy import Column, Integer, Sequence, BigInteger, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.document_has_metadata_relation import document_has_metadata_table
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationDao(OrbisBase):
    __tablename__ = 'annotation'

    annotation_id = Column(BigInteger, Sequence('annotation_id_seq'), primary_key=True)
    key = Column(Text)
    annotation_type_id = Column(BigInteger, ForeignKey('annotation_type.type_id'), nullable=False)
    annotation_type = relationship('AnnotationTypeDao', back_populates='annotations')
    annotator_id = Column(Integer, ForeignKey('annotator.annotator_id'), nullable=False)
    annotator = relationship('AnnotatorDao', back_populates='annotations')
    # data = relationship('MetadataDao', secondary=document_has_metadata_table, back_populates='annotation')
    run_has_documents = relationship('DocumentHasAnnotationDao', back_populates='annotation')
    surface_forms = Column(ARRAY(Text), nullable=False)
    start_indices = Column(ARRAY(Integer), nullable=False)
    end_indices = Column(ARRAY(Integer), nullable=False)
    # TODO, anf 02.11.2022: add constraint for equal array size
