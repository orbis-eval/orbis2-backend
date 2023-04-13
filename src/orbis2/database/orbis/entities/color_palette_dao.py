from typing import List

from sqlalchemy import Sequence, Integer, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from orbis2.database.orbis.orbis_base import OrbisBase


class ColorPaletteDao(OrbisBase):
    __tablename__ = 'color_palette'

    palette_id: Mapped[int] = mapped_column(Integer, Sequence('color_palette_id_seq'), primary_key=True)
    name: Mapped[str]
    colors: Mapped[List[int]] = mapped_column(ARRAY(Integer))

    @staticmethod
    def get_default_color_palettes():
        """
        Returns:
            Default color palettes created on https://coolors.co/.
        """
        default = ColorPaletteDao(name='default', colors=[0x533A71, 0x6184D8, 0x50C5B7, 0x9CEC5B, 0xF0F465])
        blueish = ColorPaletteDao(name='bluish', colors=[0x222E50, 0x007991, 0x439A86, 0xBCD8C1, 0xE9D985])
        return [default, blueish]
