from datetime import datetime
from sqlalchemy import ForeignKey, Column, TIMESTAMP, BigInteger, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentHasAnnotationDao(OrbisBase):
    __tablename__ = 'document_has_annotation'

    run_id = Column(BigInteger, primary_key=True)
    document_id = Column(BigInteger, primary_key=True)
    __table_args__ = (ForeignKeyConstraint((run_id, document_id),
                                           [RunHasDocumentDao.run_id, RunHasDocumentDao.document_id]),
                      {})
    annotation_id = Column(ForeignKey(AnnotationDao.annotation_id), primary_key=True)
    annotation = relationship(AnnotationDao)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
