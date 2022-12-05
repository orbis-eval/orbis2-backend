from sqlalchemy import Column, Text, Sequence, BigInteger

from orbis2.database.orbis.orbis_base import OrbisBase


class MetadataDao(OrbisBase):
    __tablename__ = 'metadata'

    metadata_id = Column(BigInteger, Sequence('metadata_id_seq'), primary_key=True)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
