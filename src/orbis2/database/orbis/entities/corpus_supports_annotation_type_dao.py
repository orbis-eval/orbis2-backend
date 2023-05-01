from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusSupportsAnnotationTypeDao(OrbisBase):
    __tablename__ = 'corpus_supports_annotation_type'

    corpus_id: Mapped[int] = mapped_column(ForeignKey(CorpusDao.corpus_id), primary_key=True)
    annotation_type_id: Mapped[int] = mapped_column(ForeignKey(AnnotationTypeDao.type_id),
                                                    primary_key=True)
    color_id: Mapped[int] = mapped_column(Sequence('corpus_supports_annotation_type_seq', cycle=True))

    annotation_type: Mapped[AnnotationTypeDao] = relationship()

    def __repr__(self):
        return f'<CorpusSupportsAnnotationTypeDao corpus_id: {self.corpus_id}, annotation_type_id: ' \
               f'{self.annotation_type_id}, color_id: {self.color_id}>'