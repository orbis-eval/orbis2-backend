from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_base import OrbisBase


class RunHasDocumentDao(OrbisBase):
    __tablename__ = 'run_has_document'

    run_id = Column(ForeignKey('run.run_id'), primary_key=True)
    run = relationship(RunDao, back_populates='documents')
    document_id = Column(ForeignKey('document.document_id'), primary_key=True)
    document = relationship('DocumentDao', back_populates='runs')
    annotations = relationship('DocumentHasAnnotationDao', back_populates='run_has_document')
    done = Column(Boolean)
