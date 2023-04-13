from sqlalchemy import Sequence
from sqlalchemy.orm import Mapped, mapped_column

from orbis2.database.orbis.orbis_base import OrbisBase


class ColorDao(OrbisBase):
    __tablename__ = 'color'

    color_id: Mapped[int] = mapped_column(Sequence('color_id_seq'), primary_key=True)
    color: Mapped[int]
