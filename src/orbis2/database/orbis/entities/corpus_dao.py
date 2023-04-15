from typing import List

from sqlalchemy import VARCHAR, Sequence
from sqlalchemy.orm import relationship, Mapped, mapped_column

from orbis2.database.orbis.orbis_base import OrbisBase


class CorpusDao(OrbisBase):
    __tablename__ = 'corpus'

    corpus_id: Mapped[int] = mapped_column(Sequence('corpus_id_seq'), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(40), nullable=False)
    supported_annotation_types: Mapped[List['CorpusSupportsAnnotationTypeDao']] = relationship(
        cascade="all, delete-orphan")
