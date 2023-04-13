from typing import List

from sqlalchemy import Sequence, Integer, Table, Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orbis2.database.orbis.entities.color_dao import ColorDao
from orbis2.database.orbis.orbis_base import OrbisBase

color_palette_has_color_table = Table(
    'color_palette_has_color',
    OrbisBase.metadata,
    Column('palette_id', ForeignKey('color_palette.palette_id')),
    Column('color_id', ForeignKey('color.color_id')),
    PrimaryKeyConstraint('palette_id', 'color_id')
)


class ColorPaletteDao(OrbisBase):
    __tablename__ = 'color_palette'

    palette_id: Mapped[int] = mapped_column(Integer, Sequence('color_palette_id_seq'), primary_key=True)
    name: Mapped[str]
    colors: Mapped[List[ColorDao]] = relationship(secondary=color_palette_has_color_table)

    @staticmethod
    def get_default_color_palettes():
        """
        Returns:
            Default color palettes created on https://coolors.co/.
        """
        default = [
            ColorDao(color=0x533A71),
            ColorDao(color=0x6184D8),
            ColorDao(color=0x50C5B7),
            ColorDao(color=0x9CEC5B),
            ColorDao(color=0xF0F465)
        ]
        default_palette = ColorPaletteDao(name='default')
        default_palette.colors = default

        blueish = [
            ColorDao(color=0x222E50),
            ColorDao(color=0x007991),
            ColorDao(color=0x439A86),
            ColorDao(color=0xBCD8C1),
            ColorDao(color=0xE9D985)
        ]
        blueish_palette = ColorPaletteDao(name='blueish')
        blueish_palette.colors = default

        return default + blueish + [default_palette, blueish_palette]
