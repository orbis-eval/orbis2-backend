from sqlalchemy import Sequence, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from orbis2.database.orbis.orbis_base import OrbisBase


class MetadataDao(OrbisBase):
    __tablename__ = 'metadata'

    metadata_id: Mapped[int] = mapped_column(BigInteger, Sequence('metadata_id_seq'), primary_key=True)
    key: Mapped[str]
    value: Mapped[str]
