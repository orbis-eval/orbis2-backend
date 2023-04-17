from operator import attrgetter

from orbis2.database.orbis.entities.color_palette_dao import ColorPaletteDao
from orbis2.database.orbis.orbis_db import OrbisDb


# noinspection PyPep8Naming
def test_get_color_palette(insert_test_data_orbis):
    """
    Verify that the database returns the standard palettes and colors.
    """
    orbis_db = OrbisDb()
    palettes = orbis_db.get_color_palettes()

    assert len(palettes) == len(ColorPaletteDao.get_default_color_palettes())
    assert [palette.name for palette in palettes] == [cp.name for cp in ColorPaletteDao.get_default_color_palettes()]
    assert [palette.colors for palette in sorted(palettes, key=attrgetter('name'))] == \
           [palette.colors for palette in sorted(ColorPaletteDao.get_default_color_palettes(),
                                                 key=attrgetter('name'))]


def test_set_corpus_annotation_type_color(insert_test_data_orbis):
    """
    Verifies that setting the corpus annotation_type color_id works.
    """
    orbis_db = OrbisDb()
    run = orbis_db.get_runs()[0]

    supported_annotation_type = run.corpus.supported_annotation_types[0].annotation_type

    # set color_ids
    for color_id in range(0, 5):
        orbis_db.set_corpus_annotation_type_color(run.corpus.corpus_id,
                                                  supported_annotation_type.type_id,
                                                  color_id)
        run = orbis_db.get_runs()[0]
        assert run.corpus.supported_annotation_types[0].color_id == color_id
