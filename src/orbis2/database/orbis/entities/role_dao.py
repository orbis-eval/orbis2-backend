from sqlalchemy import Sequence, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from orbis2.database.orbis.orbis_base import OrbisBase


class RoleDao(OrbisBase):
    __tablename__ = 'role'

    role_id: Mapped[int] = mapped_column(BigInteger, Sequence('role_id_seq'), primary_key=True)
    name: Mapped[str]
