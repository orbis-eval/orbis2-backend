"""
Test color support (i.e., work with color palettes and changing annotation coloring.
"""

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.database.orbis.entities.color_palette_dao import ColorPaletteDao


def test_get_color_palette(insert_test_data_orbis):
    """
    Verify that the color palettes retrieved from the Web service are identical with the default palettes defined
    in the ColorPaletteDao.
    """
    color_palettes = OrbisService().get_color_palettes()
    assert len(color_palettes) == len(ColorPaletteDao.get_default_color_palettes())
    for color_palette, default_color_palette in zip(color_palettes, ColorPaletteDao.get_default_color_palettes()):
        assert color_palette.colors == default_color_palette.colors


def test_set_corpus_annotation_type_color(insert_test_data_orbis):
    """
    Verify that the `set_corpus_annotation_type_color` method works correctly.
    """
    run = OrbisService().get_run_by_name('run1')
    corpus = run.corpus
    annotation_type = list(run.corpus.supported_annotation_types)[0]

    for color in range(5):
        OrbisService().set_corpus_annotation_type_color(corpus.identifier, annotation_type.identifier, color)
        assert OrbisService().get_corpus_annotation_types(run.corpus.identifier)[annotation_type] == color
