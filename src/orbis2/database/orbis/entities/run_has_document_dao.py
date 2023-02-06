from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_base import OrbisBase


class RunHasDocumentDao(OrbisBase):
    __tablename__ = 'run_has_document'

    run_id = Column(ForeignKey(RunDao.run_id), primary_key=True)
    document_id = Column(ForeignKey(DocumentDao.document_id), primary_key=True)
    document = relationship(DocumentDao)
    document_has_annotations = relationship('DocumentHasAnnotationDao',
                                            cascade='save-update, merge, delete, delete-orphan')
    done = Column(Boolean)
