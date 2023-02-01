from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_db import OrbisDb


# noinspection PyPep8Naming
def test_get_runs_get_run_names_by_corpus_id_ExistingDB_CorrectRunDao(insert_test_data_orbis):
    orbis_db = OrbisDb()
    corpora = orbis_db.get_corpora()
    run_list = orbis_db.get_run_names_by_corpus_id(corpora[0].corpus_id)
    assert isinstance(run_list[0], RunDao)


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsOrphanMetadata_relationShipAndMetadataAreRemoved(clear_test_data_orbis):
    orbis_db = OrbisDb()
    orbis_db.session.merge(AnnotationDao(
        annotation_id=1, key='annotation-key', surface_forms=['Text'], start_indices=[0], end_indices=[4],
        annotation_type=AnnotationTypeDao(
            type_id=11, name='type11'
        ), annotator=AnnotatorDao(
            annotator_id=111, name='Annotator111', roles=[]
        ), meta_data=[MetadataDao(
            metadata_id=1111, key='key1111', value='value1111'
        )]
    ))
    orbis_db.commit()

    assert orbis_db.remove_annotation(1)
    assert not orbis_db.get_metadata()


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsNoneOrphanMetadata_onlyRelationShipButNotMetadataIsRemoved(clear_test_data_orbis):
    orbis_db = OrbisDb()
    orbis_db.session.merge(AnnotationDao(
        annotation_id=1, key='annotation-key', surface_forms=['Text'], start_indices=[0], end_indices=[4],
        annotation_type=AnnotationTypeDao(
            type_id=11, name='type11'
        ), annotator=AnnotatorDao(
            annotator_id=111, name='Annotator111', roles=[]
        ), meta_data=[MetadataDao(
            metadata_id=1111, key='key1111', value='value1111'
        )]
    ))
    orbis_db.commit()
    orbis_db.session.merge(DocumentDao(document_id=1, content='Text 1234', key='key1', meta_data=[MetadataDao(
            metadata_id=1111, key='key1111', value='value1111'
        )]))
    orbis_db.commit()

    assert orbis_db.remove_annotation(1)
    assert len(orbis_db.get_metadata()) == 1