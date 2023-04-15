from typing import List, Union

from sqlalchemy import VARCHAR, Sequence, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusDao(OrbisBase):
    __tablename__ = 'corpus'

    corpus_id: Mapped[int] = mapped_column(Sequence('corpus_id_seq'), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(40), nullable=False)
    supported_annotation_types: Mapped[List['CorpusSupportsAnnotationTypeDao']] = relationship(
        cascade="all, delete-orphan")


class CorpusSupportsAnnotationTypeDao(OrbisBase):
    __tablename__ = 'corpus_supports_annotation_type'

    corpus_id: Mapped[CorpusDao] = mapped_column(ForeignKey(CorpusDao.corpus_id), primary_key=True)
    annotation_type_id: Mapped[AnnotationTypeDao] = mapped_column(ForeignKey(AnnotationTypeDao.type_id),
                                                                  primary_key=True)
    color_id: Mapped[int] = mapped_column(Sequence('corpus_supports_annotation_type_seq', cycle=True))

    annotation_type: Mapped[AnnotationTypeDao] = relationship()

