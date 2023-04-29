from typing import List

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.color_palette_dao import ColorPaletteDao
from orbis2.model.base_model import OrbisPydanticBaseModel


class ColorPalette(OrbisPydanticBaseModel):
    name: str
    # A list of the hexadecimal color values for the given Palette
    colors: List[str]

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other) -> bool:
        return isinstance(other, ColorPalette) and self.__hash__() == other.__hash__()

    @classmethod
    def from_color_palette_dao(cls, color_palette_dao: ColorPaletteDao) -> 'ColorPalette':
        return cls(color_palette_dao.name,
                   ['{0:06X}'.format(color) for color in color_palette_dao.colors])

    def to_dao(self) -> ColorPaletteDao:
        return ColorPaletteDao(name=self.name, colors=self.colors)

    def copy(self) -> 'ColorPalette':
        return ColorPaletteDao(self.name, self.colors)
