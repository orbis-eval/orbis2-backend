from sqlalchemy import Sequence, Column, Text, BigInteger

from orbis2.database.orbis.orbis_base import OrbisBase


class RoleDao(OrbisBase):
    __tablename__ = 'role'

    role_id = Column(BigInteger, Sequence('role_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
