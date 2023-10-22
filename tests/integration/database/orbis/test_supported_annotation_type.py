from orbis2.database.orbis.orbis_db import OrbisDb


# noinspection PyPep8Naming
def test_delete_annotation_type_annotationTypeIsUsedByCorpus_dontDeleteAnnotationType(insert_test_data_orbis):
    orbis_db = OrbisDb()
    corpus = orbis_db.get_corpora()[0]
    annotation_type = list(orbis_db.get_corpus_annotation_types(corpus_id=corpus.corpus_id).items())[0][0]

    assert not orbis_db.delete_annotation_type(annotation_type.type_id)
    assert len(orbis_db.get_corpus_annotation_types(corpus_id=corpus.corpus_id)) > 0
    assert len(orbis_db.get_corpora()) > 0
