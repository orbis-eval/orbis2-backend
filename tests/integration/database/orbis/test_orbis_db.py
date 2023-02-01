from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
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

    assert len(orbis_db.get_metadata()) == 1
    assert orbis_db.remove_annotation(1)
    assert not orbis_db.get_metadata()


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsMetadataSameMetadataAsOther_onlyRelationShipButNotMetadataIsRemoved(
        clear_test_data_orbis):
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
    orbis_db.session.merge(AnnotationDao(
        annotation_id=2, key='annotation-key2', surface_forms=['Texts'], start_indices=[0], end_indices=[5],
        annotation_type=AnnotationTypeDao(
            type_id=11, name='type11'
        ), annotator=AnnotatorDao(
            annotator_id=111, name='Annotator111', roles=[]
        ), meta_data=[MetadataDao(
            metadata_id=1111, key='key1111', value='value1111'
        )]
    ))
    orbis_db.commit()

    assert len(orbis_db.get_metadata()) == 1
    assert orbis_db.remove_annotation(1)
    assert len(orbis_db.get_metadata()) == 1


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsNoneOrphanMetadata_onlyRelationShipButNotMetadataIsRemoved(
        clear_test_data_orbis):
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

    assert len(orbis_db.get_metadata()) == 1
    assert orbis_db.remove_annotation(1)
    assert len(orbis_db.get_metadata()) == 1


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsTwoOrphanMetadata_relationShipAndAllMetadataAreRemoved(
        clear_test_data_orbis):
    orbis_db = OrbisDb()
    orbis_db.session.merge(AnnotationDao(
        annotation_id=1, key='annotation-key', surface_forms=['Text'], start_indices=[0], end_indices=[4],
        annotation_type=AnnotationTypeDao(
            type_id=11, name='type11'
        ), annotator=AnnotatorDao(
            annotator_id=111, name='Annotator111', roles=[]
        ), meta_data=[
            MetadataDao(
                metadata_id=1111, key='key1111', value='value1111'
            ),
            MetadataDao(
                metadata_id=1112, key='key1112', value='value1112'
            )
        ]
    ))
    orbis_db.commit()

    assert len(orbis_db.get_metadata()) == 2
    assert orbis_db.remove_annotation(1)
    assert not orbis_db.get_metadata()


# noinspection PyPep8Naming
def test_remove_annotation_annotationContainsTwoOrphanMetadata_bothRelationShipAndOnlyOneMetadataIsRemoved(
        clear_test_data_orbis):
    orbis_db = OrbisDb()
    orbis_db.session.merge(AnnotationDao(
        annotation_id=1, key='annotation-key', surface_forms=['Text'], start_indices=[0], end_indices=[4],
        annotation_type=AnnotationTypeDao(
            type_id=11, name='type11'
        ), annotator=AnnotatorDao(
            annotator_id=111, name='Annotator111', roles=[]
        ), meta_data=[
            MetadataDao(
                metadata_id=1111, key='key1111', value='value1111'
            ),
            MetadataDao(
                metadata_id=1112, key='key1112', value='value1112'
            )
        ]
    ))
    orbis_db.commit()
    orbis_db.session.merge(DocumentDao(document_id=1, content='Text 1234', key='key1', meta_data=[MetadataDao(
            metadata_id=1111, key='key1111', value='value1111'
        )]))
    orbis_db.commit()

    assert len(orbis_db.get_metadata()) == 2
    assert orbis_db.remove_annotation(1)
    assert len(orbis_db.get_metadata()) == 1


# noinspection PyPep8Naming
def test_remove_annotation_from_document_annotationIsOrphanAfterwards_annotationIsRemoved(insert_test_data_orbis):
    orbis_db = OrbisDb()
    run = orbis_db.get_runs()[0]
    document = run.run_has_documents[0].document
    annotation = run.run_has_documents[0].document_has_annotations[0].annotation

    assert len(orbis_db.get_metadata()) == 2
    assert len(orbis_db.get_annotations()) == 1
    assert orbis_db.remove_annotation_from_document(DocumentHasAnnotationDao(
        run_id=run.run_id, document_id=document.document_id, annotation_id=annotation.annotation_id
    ))
    assert not orbis_db.get_annotations()
    assert len(orbis_db.get_metadata()) == 1


# noinspection PyPep8Naming
def test_remove_annotation_from_document_annotationIsNotOrphanAfterwards_annotationIsNotRemoved(clear_test_data_orbis):
    orbis_db = OrbisDb()
    result = orbis_db.session.merge(
        RunDao(run_id=1, name='run1', description='run1',
               run_has_documents=[
                   RunHasDocumentDao(
                       document=DocumentDao(document_id=1, content='Text 1234', key='doc-key', meta_data=[]),
                       document_has_annotations=[
                           DocumentHasAnnotationDao(
                               annotation=AnnotationDao(
                                   annotation_id=1, key='annotation-key1', surface_forms=['Text'], start_indices=[0],
                                   end_indices=[4],
                                   annotation_type=AnnotationTypeDao(
                                       type_id=11, name='type11'
                                   ), annotator=AnnotatorDao(
                                       annotator_id=111, name='Annotator111', roles=[]
                                   ), meta_data=[
                                       MetadataDao(
                                           metadata_id=1111, key='key1111', value='value1111'
                                       )
                                   ]
                               )
                           ),
                           DocumentHasAnnotationDao(
                               annotation=AnnotationDao(
                                   annotation_id=2, key='annotation-key2', surface_forms=['Texts'], start_indices=[0],
                                   end_indices=[5],
                                   annotation_type=AnnotationTypeDao(
                                       type_id=11, name='type11'
                                   ), annotator=AnnotatorDao(
                                       annotator_id=111, name='Annotator111', roles=[]
                                   ), meta_data=[
                                       MetadataDao(
                                           metadata_id=1111, key='key1111', value='value1111'
                                       )
                                   ]
                               )
                           )
                       ]
                   )
               ],
               corpus=CorpusDao(corpus_id=1, name='corpus1'))
    )
    result = orbis_db.commit()

    assert len(orbis_db.get_annotations()) == 2
    assert len(orbis_db.get_metadata()) == 1
    assert orbis_db.remove_annotation_from_document(DocumentHasAnnotationDao(
        run_id=1, document_id=1, annotation_id=1
    ))
    assert len(orbis_db.get_annotations()) == 1
    assert len(orbis_db.get_metadata()) == 1
