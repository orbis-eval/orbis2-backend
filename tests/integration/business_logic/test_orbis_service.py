from xxhash import xxh32_hexdigest

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role
from orbis2.model.run import Run


# noinspection PyPep8Naming
def test_get_runs_dbExistsAndContainsRuns_getAllRunsCorrectlyTransformed(insert_test_data_orbis):
    runs = OrbisService().get_runs()

    assert len(runs) == 1
    run = runs[0]
    assert type(run) is Run
    assert run._id > 0
    assert run.name == 'run1'
    assert type(run.corpus) is Corpus
    assert run.corpus._id > 0
    assert run.corpus.name == 'corpus1'

    assert len(run.corpus.supported_annotation_types) == 1
    supported_annotation_type = list(run.corpus.supported_annotation_types.items())[0][0]
    assert type(supported_annotation_type) is AnnotationType
    assert supported_annotation_type._id > 0
    assert supported_annotation_type.name == 'annotation-type1'

    documents = list(run.document_annotations.keys())
    assert len(documents) == 1
    document = documents[0]
    assert type(document) is Document
    assert document._id > 0
    assert document.content == 'Text, das ist ein Beispiel'

    assert len(document.metadata) == 1
    metadata = document.metadata[0]
    assert type(metadata) is Metadata
    assert metadata._id > 0
    assert metadata.value == 'value1'
    assert metadata.key == 'key1'

    annotations = list(run.document_annotations[document])
    assert len(annotations) == 1
    annotation = annotations[0]
    assert type(annotation) is Annotation
    assert annotation._id > 0
    assert annotation.key == 'url'
    assert annotation.surface_forms[0] == 'Text'
    assert annotation.start_indices[0] == 0
    assert annotation.end_indices[0] == 4
    assert type(annotation.annotation_type) is AnnotationType
    assert annotation.annotation_type._id > 0
    assert annotation.annotation_type.name == 'annotation-type1'
    assert type(annotation.annotator) is Annotator
    assert annotation.annotator._id > 0
    assert annotation.annotator.name == 'Andreas'
    assert annotation.annotator.password == xxh32_hexdigest('test1234')

    assert len(annotation.annotator.roles) == 1
    role = annotation.annotator.roles[0]
    assert role._id > 0
    assert role.name == 'admin'

    assert len(annotation.metadata) == 1
    metadata = annotation.metadata[0]
    assert type(metadata) is Metadata
    assert metadata._id > 0
    assert metadata.value == 'value2'
    assert metadata.key == 'key2'


# noinspection PyPep8Naming
def test_get_run_by_name_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    run = OrbisService().get_run_by_name('run1')

    assert run
    assert run._id > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_run_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    run_id = OrbisService().get_runs()[0]._id
    run = OrbisService().get_run(run_id)

    assert run
    assert run._id > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_run_by_corpus_id_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    corpus_id = OrbisService().get_corpora()[0]._id
    runs = OrbisService().get_runs_by_corpus_id(corpus_id)

    assert runs
    assert len(runs) == 1
    run = runs[0]
    assert run._id > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_documents_of_corpus_dbExistsAndContainsCorpus_returnDocuments(insert_test_data_orbis):
    corpus_id = OrbisService().get_corpora()[0]._id
    documents = OrbisService().get_documents_of_corpus(corpus_id)

    assert len(documents) == 1
    assert documents[0].content == 'Text, das ist ein Beispiel'


# noinspection PyPep8Naming
def test_get_documents_of_corpus_dbExistsAndContainsMultipleCorpus_returnDocumentsOfCorrectCorpus(
        insert_test_data_orbis):
    corpus_id = OrbisService().get_corpora()[0]._id
    documents = OrbisService().get_documents_of_corpus(corpus_id)

    assert len(documents) == 1

    OrbisService().add_run(
        Run(
            'run2', 'run2', Corpus('corpus2', {AnnotationType('annotation-type1'): 1}),
            {Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')]):
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]}))

    documents = OrbisService().get_documents_of_corpus(corpus_id)

    assert len(documents) == 1
    assert documents[0].content == 'Text, das ist ein Beispiel'


# noinspection PyPep8Naming
def test_get_documents_of_corpus_corpusContainsTwoDocumentsPageSize1_returnOnlyFirstDocumentOfCorrectCorpus(
        clear_test_data_orbis):
    corpus =  Corpus('corpus1', {AnnotationType('annotation-type1'): 1})
    document1 = Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')])
    document2 = Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')])
    OrbisService().add_run(
        Run(
            'run1', 'run1', corpus,
            {document1:
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
             document2:
                 [Annotation('url', 'Texts', 0, 5, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]
             }))

    documents = OrbisService().get_documents_of_corpus(corpus._id, 1, 0)
    assert len(documents) == 1
    assert documents[0]._id == document1._id


# noinspection PyPep8Naming
def test_get_documents_of_corpus_corpusContainsTwoDocumentsSkipFirstPageSize1_returnSecondDocumentOfCorrectCorpus(
        clear_test_data_orbis):
    corpus =  Corpus('corpus1', {AnnotationType('annotation-type1'): 1})
    document1 = Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')])
    document2 = Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')])
    OrbisService().add_run(
        Run(
            'run1', 'run1', corpus,
            {document1:
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
             document2:
                 [Annotation('url', 'Texts', 0, 5, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]
             }))

    documents = OrbisService().get_documents_of_corpus(corpus._id, 1, 1)
    assert len(documents) == 1
    assert documents[0]._id == document2._id


# noinspection PyPep8Naming
def test_get_documents_of_corpus_corpusContainsTwoDocumentsSkipFirstPageSizeNone_returnSecondDocumentOfCorrectCorpus(
        clear_test_data_orbis):
    corpus =  Corpus('corpus1', [AnnotationType('annotation-type1')])
    document1 = Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')])
    document2 = Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')])
    OrbisService().add_run(
        Run(
            'run1', 'run1', corpus,
            {document1:
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
             document2:
                 [Annotation('url', 'Texts', 0, 5, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]
             }))

    documents = OrbisService().get_documents_of_corpus(corpus._id, skip=1)
    assert len(documents) == 1
    assert documents[0]._id == document2._id


# noinspection PyPep8Naming
def test_get_documents_of_run_dbExistsAndContainsRun_returnDocuments(insert_test_data_orbis):
    run_id = OrbisService().get_runs()[0]._id
    documents = OrbisService().get_documents_of_run(run_id)

    assert len(documents) == 1
    assert documents[0].content == 'Text, das ist ein Beispiel'


# noinspection PyPep8Naming
def test_get_documents_of_run_dbExistsAndContainsMultipleRuns_returnDocumentsOfCorrectRun(
        insert_test_data_orbis):
    run_id = OrbisService().get_runs()[0]._id
    documents = OrbisService().get_documents_of_run(run_id)

    assert len(documents) == 1

    OrbisService().add_run(
        Run(
            'run2', 'run2', Corpus('corpus2', [AnnotationType('annotation-type1')]),
            {Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')]):
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]}))

    documents = OrbisService().get_documents_of_run(run_id)

    assert len(documents) == 1
    assert documents[0].content == 'Text, das ist ein Beispiel'


# noinspection PyPep8Naming
def test_get_corpora_dbExistsAndContainsCorpus_returnsCorpus(insert_test_data_orbis):
    corpora = OrbisService().get_corpora()

    assert corpora
    assert len(corpora) == 1
    corpus = corpora[0]
    assert corpus._id > 0
    assert corpus.name == 'corpus1'


# noinspection PyPep8Naming
def test_get_corpus_id_dbExistsAndContainsCorpus_returnsCorpusId(insert_test_data_orbis):
    assert OrbisService().get_corpus_id('corpus1') > 0


# noinspection PyPep8Naming
def test_get_annotation_types_dbExistsAndContainsAnnotationTypes_returnsAnnotationTypes(insert_test_data_orbis):
    corpus = OrbisService().get_corpora()[0]
    annotation_types = OrbisService().get_corpus_annotation_types(corpus_id=corpus._id)

    assert annotation_types
    assert len(annotation_types) == 1
    annotation_type = list(annotation_types.items())[0][0]
    assert annotation_type.type_id > 0
    assert annotation_type.name == 'annotation-type1'


# noinspection PyPep8Naming
def test_get_metadata_dbExistsAndContainsMetadata_returnsMetadata(insert_test_data_orbis):
    metadata = OrbisService().get_metadata()

    assert metadata
    assert len(metadata) == 2
    metadatum = metadata[0]
    assert metadatum._id > 0
    assert metadatum.key == 'key1'
    assert metadatum.value == 'value1'


# noinspection PyPep8Naming
def test_add_annotation_to_document_surfaceFormLenDiffersFromStartIndicesLen_returnNone(insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    run_id = run._id
    document_id = list(run.document_annotations.keys())[0]._id
    annotation = Annotation('', ('test', 'text'), (0, 7, 13), (4, 11), AnnotationType('annotation-type1'),
                            Annotator('Andreas', [Role('admin')]), run_id, document_id)

    assert not OrbisService().add_annotation_to_document(annotation)


# noinspection PyPep8Naming
def test_add_annotation_to_document_surfaceFormLenDiffersFromEndIndicesLen_returnNone(insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    run_id = run._id
    document_id = list(run.document_annotations.keys())[0]._id
    annotation = Annotation('', ('test', 'text'), (0, 7), (4, 11, 18), AnnotationType('annotation-type1'),
                            Annotator('Andreas', [Role('admin')]), run_id, document_id)

    assert not OrbisService().add_annotation_to_document(annotation)


# noinspection PyPep8Naming
def test_add_annotation_to_document_annotationIsMissingDocumentId_returnNone(insert_test_data_orbis):
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1

    run_id = db_run._id
    assert not OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                    AnnotationType('annotation_type1'),
                                                                    Annotator('Andreas', []), run_id))
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1


# noinspection PyPep8Naming
def test_add_annotation_to_document_annotationIsMissingRunId_returnNone(insert_test_data_orbis):
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1

    run_id = db_run._id
    document_id = list(db_run.document_annotations.keys())[0]._id
    assert not OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                    AnnotationType('annotation_type1'),
                                                                    Annotator('Andreas', []), document_id=document_id))
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1


# noinspection PyPep8Naming
def test_add_annotation_to_document_addNewAnnotationToExistingDocument_existingDocumentContainsNewAnnotation(
        insert_test_data_orbis):
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1

    run_id = db_run._id
    document_id = list(db_run.document_annotations.keys())[0]._id
    added_annotation = OrbisService().add_annotation_to_document(Annotation(
        '', 'something', 0, 9, AnnotationType('annotation_type1'), Annotator('Andreas', []), run_id, document_id))

    assert added_annotation
    # added annotation contains now a timestamp
    assert added_annotation.timestamp is not None
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2


# noinspection PyPep8Naming
def test_add_annotation_to_document_addNewAnnotationTwice_annotationShouldBeAddedOnlyOnce(insert_test_data_orbis):
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1

    run_id = db_run._id
    document_id = list(db_run.document_annotations.keys())[0]._id
    annotation = Annotation('', 'something', 0, 9, AnnotationType('annotation_type1'),
                            Annotator('Andreas', []), run_id, document_id)
    assert OrbisService().add_annotation_to_document(annotation)
    assert OrbisService().add_annotation_to_document(annotation)
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2


# noinspection PyPep8Naming
def test_add_annotation_to_document_addTwoDifferentAnnotationWithSameMetadata_metadataShouldBeAddedOnlyOnce(
        insert_test_data_orbis):
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 1

    run_id = db_run._id
    document_id = list(db_run.document_annotations.keys())[0]._id
    annotation1 = Annotation('', 'something', 0, 9, AnnotationType('annotation_type1'),
                             Annotator('Andreas', []), run_id, document_id, [Metadata("key1", "value1")])

    annotation2 = Annotation('', 'something-else', 0, 14, AnnotationType('annotation_type2'),
                             Annotator('Andreas', []), run_id, document_id, [Metadata("key1", "value1")])
    assert OrbisService().add_annotation_to_document(annotation1)
    assert OrbisService().add_annotation_to_document(annotation2)
    db_metadata = OrbisService().get_metadata()
    # contains only one document
    assert len(db_metadata) == 2


# noinspection PyPep8Naming
def test_update_run_newDocumentHasBeenAdded_correctlyUpdatedOnDb(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')]))]}
              )
    updated_run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-tpye2')]),
                      {Document('Text, das ist ein Beispiel'):
                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                                       Annotator('Andreas', [Role('admin')]))],
                       Document('Annotation, das ist ein Beispiel'):
                           [Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                                       Annotator('Andreas', [Role('admin')]))]
                       }
                      )
    assert OrbisService().add_run(run)
    assert OrbisService().add_run(updated_run)
    updated_run_on_db = OrbisService().get_runs()[0]

    # annotations changed
    assert updated_run_on_db.document_annotations.keys() != run.document_annotations.keys()
    assert len(updated_run_on_db.document_annotations.values()) != len(run.document_annotations.values())
    assert updated_run_on_db.document_annotations.keys() == updated_run.document_annotations.keys()
    assert len(updated_run_on_db.document_annotations.values()) == len(updated_run.document_annotations.values())
    assert list(updated_run_on_db.document_annotations.values())[0] == list(
        updated_run.document_annotations.values())[0]
    assert list(updated_run_on_db.document_annotations.values())[1] == list(
        updated_run.document_annotations.values())[1]

    # other values did not change
    assert updated_run_on_db.name == run.name
    assert updated_run_on_db.description == run.description
    assert updated_run_on_db.corpus == run.corpus
    assert updated_run_on_db.parents == run.parents


# noinspection PyPep8Naming
def test_update_run_documentHasBeenDeleted_correctlyUpdatedOnDb(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')]))],
               Document('Annotation, das ist ein Beispiel'):
                   [Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    updated_run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-tpye2')]),
                      {Document('Text, das ist ein Beispiel'):
                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                                       Annotator('Andreas', [Role('admin')]))]}
                      )

    assert OrbisService().add_run(run)
    assert OrbisService().add_run(updated_run)
    updated_run_on_db = OrbisService().get_runs()[0]

    # annotations changed
    assert updated_run_on_db.document_annotations.keys() != run.document_annotations.keys()
    assert len(updated_run_on_db.document_annotations.values()) != len(run.document_annotations.values())
    assert updated_run_on_db.document_annotations.keys() == updated_run.document_annotations.keys()
    assert len(updated_run_on_db.document_annotations.values()) == len(updated_run.document_annotations.values())
    assert list(updated_run_on_db.document_annotations.values())[0] == list(
        updated_run.document_annotations.values())[0]

    # other values did not change
    assert updated_run_on_db.name == run.name
    assert updated_run_on_db.description == run.description
    assert updated_run_on_db.corpus == run.corpus
    assert updated_run_on_db.parents == run.parents


# noinspection PyPep8Naming
def test_update_run_newAnnotationHasBeenAddedToExistingDocument_correctlyUpdatedOnDb(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')]))]}
              )
    updated_run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-tpye2')]),
                      {Document('Text, das ist ein Beispiel'):
                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                                       Annotator('Andreas', [Role('admin')])),
                            Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                                       Annotator('Andreas', [Role('admin')]))]
                       }
                      )
    assert OrbisService().add_run(run)
    assert OrbisService().add_run(updated_run)
    updated_run_on_db = OrbisService().get_runs()[0]

    # annotations changed
    assert updated_run_on_db.document_annotations.keys() == run.document_annotations.keys()
    assert len(list(updated_run_on_db.document_annotations.values())[0]) != len(list(
        run.document_annotations.values())[0])
    assert len(list(updated_run_on_db.document_annotations.values())[0]) == len(list(
        updated_run.document_annotations.values())[0])
    assert list(updated_run_on_db.document_annotations.values())[0] == list(
        updated_run.document_annotations.values())[0]

    # other values did not change
    assert updated_run_on_db.name == run.name
    assert updated_run_on_db.description == run.description
    assert updated_run_on_db.corpus == run.corpus
    assert updated_run_on_db.parents == run.parents


# noinspection PyPep8Naming
def test_update_run_annotationHasBeenRemovedFromExistingDocument_correctlyUpdatedOnDb(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    updated_run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-tpye2')]),
                      {Document('Text, das ist ein Beispiel'):
                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                                       Annotator('Andreas', [Role('admin')]))]}
                      )

    assert OrbisService().add_run(run)
    assert OrbisService().add_run(updated_run)
    updated_run_on_db = OrbisService().get_runs()[0]

    # annotations changed
    assert updated_run_on_db.document_annotations.keys() == run.document_annotations.keys()
    assert len(list(updated_run_on_db.document_annotations.values())[0]) != len(list(
        run.document_annotations.values())[0])
    assert len(list(updated_run_on_db.document_annotations.values())[0]) == len(list(
        updated_run.document_annotations.values())[0])
    assert list(updated_run_on_db.document_annotations.values())[0] == list(
        updated_run.document_annotations.values())[0]

    # other values did not change
    assert updated_run_on_db.name == run.name
    assert updated_run_on_db.description == run.description
    assert updated_run_on_db.corpus == run.corpus
    assert updated_run_on_db.parents == run.parents


# noinspection PyPep8Naming
def test_get_run_names_defaultDbData_correctRunWithNamesAndId(insert_test_data_orbis):
    all_runs = OrbisService().get_run_names()
    assert len(all_runs) == 1
    assert all_runs[0].name == 'run1'
    assert isinstance(all_runs[0], Run)


# noinspection PyPep8Naming
def test_get_run_names_defaultDbData_correctRunWithNamesAndIdByCorpusId(insert_test_data_orbis):
    service = OrbisService()
    runs_by_corpus_id = service.get_run_names((service.get_corpora()[0])._id)
    assert len(runs_by_corpus_id) == 1
    assert runs_by_corpus_id[0].name == 'run1'
    assert isinstance(runs_by_corpus_id[0], Run)


#noinspection PyPep8Naming
def test_get_annotations_includingRunAndDocumentId_returnAnnotationsOfSpecificRunAndDocument(insert_test_data_orbis):
    document_under_test = Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')])
    run = Run(
        'run2', 'run2', Corpus('corpus1', [AnnotationType('annotation-type1')]),
        {
            Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
                [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                            Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
            document_under_test:
                [
                    Annotation('url', 'das', 6, 9, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
                    Annotation('url', 'Beispiel', 26, 34, AnnotationType('annotation-type2'),
                               Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])
                ]
        }
    )
    assert OrbisService().add_run(run)
    annotations = OrbisService().get_annotations(run._id, document_under_test._id)
    assert len(annotations) == 2
    assert annotations[0].surface_forms[0] == 'Beispiel'
    assert annotations[0].run_id is not None
    assert annotations[0].document_id is not None
    assert annotations[0].timestamp is not None
    assert annotations[1].surface_forms[0] == 'das'
    assert annotations[1].run_id is not None
    assert annotations[1].document_id is not None
    assert annotations[1].timestamp is not None


#noinspection PyPep8Naming
def test_remove_annotation_from_document_removeAnnotationFromExistingDocument_documentContainsNoMoreAnnotations(
        insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    document = list(run.document_annotations.keys())[0]
    annotation = run.document_annotations[document][0]

    assert annotation
    assert OrbisService().remove_annotation_from_document(annotation)
    assert len(OrbisService().get_annotations()) == 0


# TODO, anf 26.01.2023: run with two different documents but same annotation should add annotation
#  once to run1-document1-annotation1 and once to run1-document2-annotation1 combination but that doesn't work,
#  should it, is there a case like this?
# #noinspection PyPep8Naming
# def test_get_annotations_includingRunAndDocumentId_returnAnnotationsOfSpecificRunAndDocument(insert_test_data_orbis):
#     document_under_test = Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')])
#     run = Run(
#         'run2', 'run2', Corpus('corpus1', [AnnotationType('annotation-type1')]),
#         {
#             Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
#                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
#                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
#             document_under_test:
#                 [
#                     Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
#                                Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
#                     Annotation('url', 'Beispiel', 26, 34, AnnotationType('annotation-type2'),
#                                Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])
#                 ]
#         }
#     )
#     assert OrbisService().add_run(run)
#     annotations = OrbisService().get_annotations(run._id, document_under_test._id)
#     assert len(annotations) == 2
#     assert annotations[0].surface_forms[0] == 'Text'
#     assert annotations[1].surface_forms[0] == 'Beispiel'
