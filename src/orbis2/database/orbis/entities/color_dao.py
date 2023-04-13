from sqlalchemy import Column, BigInteger, Sequence

from orbis2.database.orbis.orbis_base import OrbisBase


class ColorDao(OrbisBase):
    __tablename__ = 'color'

    color_id = Column(BigInteger, Sequence('color_id_seq'), primary_key=True)
    color = Column(BigInteger, nullable=False)
