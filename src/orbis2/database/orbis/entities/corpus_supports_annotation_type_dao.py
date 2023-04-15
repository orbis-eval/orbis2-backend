from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusSupportsAnnotationTypeDao(OrbisBase):
    __tablename__ = 'corpus_supports_annotation_type'

    corpus_id: Mapped[CorpusDao] = mapped_column(ForeignKey(CorpusDao.corpus_id), primary_key=True)
    annotation_type_id: Mapped[AnnotationTypeDao] = mapped_column(ForeignKey(AnnotationTypeDao.type_id),
                                                                  primary_key=True)
    color_id: Mapped[int] = mapped_column(Sequence('corpus_supports_annotation_type_seq', cycle=True))

    annotation_type: Mapped[AnnotationTypeDao] = relationship()
