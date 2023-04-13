from sqlalchemy import Column, Sequence, Text, Integer

from orbis2.database.orbis.orbis_base import OrbisBase


class ColorPaletteDao(OrbisBase):
    __tablename__ = 'color_palette'

    palette_id = Column(Integer, Sequence('color_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
