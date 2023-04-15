from datetime import datetime
from sqlalchemy import ForeignKey, Column, TIMESTAMP, BigInteger, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentHasAnnotationDao(OrbisBase):
    __tablename__ = 'document_has_annotation'

    run_id = Column(BigInteger, primary_key=True, default=0)        # note: the default values only serve to prevent
    document_id = Column(BigInteger, primary_key=True, default=0)   # SQLAlechemy warnings.
    # cascading in table_args removes entries from this table, when entries (run_id, document_id) from parent table
    # (run_has_document) get deleted
    __table_args__ = (ForeignKeyConstraint((run_id, document_id),
                                           [RunHasDocumentDao.run_id, RunHasDocumentDao.document_id],
                                           onupdate='CASCADE', ondelete='CASCADE'),
                      {})
    annotation_id = Column(ForeignKey(AnnotationDao.annotation_id), primary_key=True)
    annotation = relationship(AnnotationDao)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
