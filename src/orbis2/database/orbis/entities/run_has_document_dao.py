from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_base import OrbisBase
if TYPE_CHECKING:
    from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao


class RunHasDocumentDao(OrbisBase):
    __tablename__ = 'run_has_document'

    run_id: Mapped[int] = mapped_column(ForeignKey(RunDao.run_id), primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey(DocumentDao.document_id), primary_key=True)
    document: Mapped[DocumentDao] = relationship()
    document_has_annotations: Mapped[List[DocumentHasAnnotationDao]] = relationship(
        cascade='save-update, merge, delete, delete-orphan')
    done = Column(Boolean)
