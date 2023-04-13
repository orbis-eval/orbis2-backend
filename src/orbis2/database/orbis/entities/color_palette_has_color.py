from sqlalchemy import Column, ForeignKey, Table

from orbis2.database.orbis.entities.color_dao import ColorDao
from orbis2.database.orbis.entities.color_palette_dao import ColorPaletteDao
from orbis2.database.orbis.orbis_base import OrbisBase

color_palette_has_color_table = Table(
    'color_palette_has_color',
    OrbisBase.metadata,
    Column('palette_id', ForeignKey('color_palette.palette_id'), primary_key=True),
    Column('color_id', ForeignKey('color.color_id'), primary_key=True),
)


def default_color_palettes():
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
    default_palette.color = default

    blueish = [
        ColorDao(color=0x222E50),
        ColorDao(color=0x007991),
        ColorDao(color=0x439A86),
        ColorDao(color=0xBCD8C1),
        ColorDao(color=0xE9D985)
    ]
    blueish_palette = ColorPaletteDao(name='blueish')
    blueish_palette.color = default

    return default + blueish + [default_palette, blueish_palette]
