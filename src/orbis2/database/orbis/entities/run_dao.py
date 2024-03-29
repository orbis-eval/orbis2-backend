from __future__ import annotations
from typing import List, TYPE_CHECKING
import datetime

from sqlalchemy import Sequence, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.run_derived_from_relation import run_derived_from_table
from orbis2.database.orbis.orbis_base import OrbisBase

if TYPE_CHECKING:
    from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao


class RunDao(OrbisBase):
    __tablename__ = 'run'

    run_id: Mapped[int] = mapped_column(BigInteger, Sequence('run_id_seq'), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    run_has_documents: Mapped[List[RunHasDocumentDao]] = relationship(
        cascade='save-update, merge, delete, delete-orphan')
    corpus_id: Mapped[int] = mapped_column(ForeignKey(CorpusDao.corpus_id))
    corpus: Mapped[CorpusDao] = relationship()
    parents: Mapped[List['RunDao']] = relationship(secondary=run_derived_from_table,
                                                   primaryjoin=run_derived_from_table.c.parent_id == run_id,
                                                   secondaryjoin=run_derived_from_table.c.child_id == run_id)
    is_gold_standard: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    current_gold_standard_id: Mapped[int] = mapped_column(ForeignKey('run.run_id'), nullable=True)
    current_gold_standard: Mapped['RunDao'] = relationship("RunDao", remote_side=[run_id])
