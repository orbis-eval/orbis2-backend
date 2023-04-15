from sqlalchemy import BigInteger, Sequence
from sqlalchemy.orm import mapped_column, Mapped

from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotationTypeDao(OrbisBase):
    __tablename__ = 'annotation_type'

    type_id: Mapped[int] = mapped_column(BigInteger, Sequence('annotation_type_id_seq'), primary_key=True)
    name: Mapped[str]
