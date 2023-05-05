from typing import Optional

from sqlalchemy import Sequence, BigInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped

from orbis2.database.orbis.entities.annotator_has_role_relation import annotator_has_role_table
from orbis2.database.orbis.entities.role_dao import RoleDao
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotatorDao(OrbisBase):
    __tablename__ = 'annotator'

    annotator_id: Mapped[int] = mapped_column(BigInteger, Sequence('annotator_id_seq'), primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    roles: Mapped[RoleDao] = relationship(secondary=annotator_has_role_table)
