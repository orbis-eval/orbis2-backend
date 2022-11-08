from datetime import datetime
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentHasAnnotationDao(OrbisBase):
    __tablename__ = 'document_has_annotation'

    run_has_document_id = Column(ForeignKey('run_has_document.run_id', 'run_has_document.document_id'), primary_key=True)
    run_has_document = relationship('RunHasDocumentDao', back_populates='annotations')
    annotation_id = Column(ForeignKey('annotation.annotation_id'), primary_key=True)
    annotation = relationship('AnnotationDao', back_populates='run_has_documents')


    # run = relationship('RunDao', back_populates='documents')
    # document_id = Column(ForeignKey('document.document_id'), primary_key=True)
    # annotation_id = Column(ForeignKey('annotation.annotation_id'), primary_key=True)
    # timestamp = Column(TIMESTAMP, default=datetime.utcnow)
