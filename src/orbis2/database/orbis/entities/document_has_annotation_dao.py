from datetime import datetime
from sqlalchemy import ForeignKey, Column, TIMESTAMP, BigInteger, ForeignKeyConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentHasAnnotationDao(OrbisBase):
    __tablename__ = 'document_has_annotation'

    # note: the default values only serve to prevent SQL Alchemy warnings.
    run_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=0)
    document_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=0)
    # cascading in table_args deletes entries from this table, when entries (run_id, document_id) from parent table
    # (run_has_document) get deleted
    __table_args__ = (ForeignKeyConstraint((run_id, document_id),
                                           [RunHasDocumentDao.run_id, RunHasDocumentDao.document_id],
                                           onupdate='CASCADE', ondelete='CASCADE'),
                      {})
    annotation_id: Mapped[int] = mapped_column(ForeignKey(AnnotationDao.annotation_id), primary_key=True)
    annotation: Mapped[AnnotationDao] = relationship()
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
