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
    supported_annotation_type = run.corpus.supported_annotation_types[0]
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
            'run2', 'run2', Corpus('corpus2', [AnnotationType('annotation-type1')]),
            {Document('Text, das ist ein anderes Beispiel', metadata=[Metadata('key1', 'value1')]):
                 [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                             Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]}))

    documents = OrbisService().get_documents_of_corpus(corpus_id)

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
    annotation_types = OrbisService().get_annotation_types()

    assert annotation_types
    assert len(annotation_types) == 1
    annotation_type = annotation_types[0]
    assert annotation_type._id > 0
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
def test_add_runs_emptyDbExistsAndRunIsCorrectlyInitialized_returnTrue(clear_test_data_orbis):
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                               AnnotationType('annotation-tpye2')]),
            {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])]}
            )])


# noinspection PyPep8Naming
def test_add_runs_emptyDbExistsAndRunWithMultipleAnnotationsIsCorrectlyInitialized_returnTrue(
        clear_test_data_orbis):
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'), AnnotationType('annotation-type2')]),
            {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')]),
              Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                         Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key1', 'value1'),
                                                                          Metadata('key2', 'value2')])
              ]}
            )])


# noinspection PyPep8Naming
def test_add_runs_emptyDbExistsAndRunWithMultipleDocumentAnnotationsIsCorrectlyInitialized_returnTrue(
        clear_test_data_orbis):
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'), AnnotationType('annotation-type2')]),
            {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')]),
              Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                         Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])],
             Document('Text2, das ist ein neues Beispiel2', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text2', 0, 5, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')]),
              Annotation('', 'Beispiel2', 25, 34, AnnotationType('annotation-type2'),
                         Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])]
             }
            )])


# noinspection PyPep8Naming
def test_add_runs_addMultipleRunsContainingAnnotationsWithSameTypeInOneCall_annotationTypeIsInsertedOnlyOnce(
        clear_test_data_orbis):
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
            {Document('Text, das ist ein Beispiel'):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]))]}
            ),
        Run('Run2', 'Run2', Corpus('Corpus2', [AnnotationType('annotation-type1')]),
            {Document('Annotation, das ist ein Beispiel'):
             [Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                         Annotator('Andreas', [Role('admin')]))]}
            )])
    annotation_types = OrbisService().get_annotation_types()

    assert len(annotation_types) == 1
    assert annotation_types[0].name == 'annotation-type1'


# noinspection PyPep8Naming
def test_add_runs_addMultipleRunsWithSameMetadataInOneCall_metadataIsInsertedOnlyOnce(
        clear_test_data_orbis):
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
            {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1')]),
              Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type1'),
                         Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1')])],
             Document('Text2, das ist ein neues Beispiel2', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text2', 0, 5, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                         metadata=[Metadata('key1', 'value1')])]
             }
            )])
    metadata = OrbisService().get_metadata()

    assert len(metadata) == 1
    assert metadata[0].key == 'key1'
    assert metadata[0].value == 'value1'


# noinspection PyPep8Naming
def test_add_run_addSameRunTwice_allDataAreInsertedOnlyOnce(
        clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
              {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
               [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                           metadata=[Metadata('key1', 'value1')])]})
    assert OrbisService().add_run(run)
    assert OrbisService().add_run(run)

    runs = OrbisService().get_runs()
    assert len(runs) == 1

    documents = OrbisService().get_documents()
    assert len(documents) == 1

    annotations = OrbisService().get_annotations()
    assert len(annotations) == 1

    corpora = OrbisService().get_corpora()
    assert len(corpora) == 1

    annotation_types = OrbisService().get_annotation_types()
    assert len(annotation_types) == 1

    metadata = OrbisService().get_metadata()
    assert len(metadata) == 1

    annotators = OrbisService().get_annotators()
    assert len(annotators) == 1


# noinspection PyPep8Naming
def test_add_run_addSameRunFromDb_allDataAreInsertedOnlyOnce(insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    assert OrbisService().add_run(run)

    runs = OrbisService().get_runs()
    assert len(runs) == 1

    documents = OrbisService().get_documents()
    assert len(documents) == 1

    annotations = OrbisService().get_annotations()
    assert len(annotations) == 1

    corpora = OrbisService().get_corpora()
    assert len(corpora) == 1

    annotation_types = OrbisService().get_annotation_types()
    assert len(annotation_types) == 1

    metadata = OrbisService().get_metadata()
    assert len(metadata) == 2

    annotators = OrbisService().get_annotators()
    assert len(annotators) == 1


# noinspection PyPep8Naming
def test_add_run_runContainsAnnotationWithAlreadyExistingType_annotationTypeIsNotInsertedAndNoErrorOccurs(
        clear_test_data_orbis):
    assert OrbisService().add_run(Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                      {Document('Text, das ist ein Beispiel'):
                                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]))]}
                                      ))
    assert OrbisService().add_run(Run('Run2', 'Run2', Corpus('Corpus2', [AnnotationType('annotation-type1')]),
                                      {Document('Annotation, das ist ein Beispiel'):
                                           [Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]))]}
                                      ))
    annotation_types = OrbisService().get_annotation_types()

    assert len(annotation_types) == 1
    assert annotation_types[0].name == 'annotation-type1'


# noinspection PyPep8Naming
def test_add_run_runHasParent_childIsReferencedInParent(insert_test_data_orbis):
    parent = OrbisService().get_runs()[0]
    child = parent.copy('child-run', 'child-run')

    assert OrbisService().add_run(child)

    runs = OrbisService().get_runs()

    assert len(runs) == 2

    db_parent = [run for run in runs if run.name == 'run1'][0]
    db_child = [run for run in runs if run.name == 'child-run'][0]

    assert db_child == child
    assert len(db_child.parents) == 1
    assert db_child.parents[0] == parent
    assert parent == db_parent

    assert db_child.document_annotations == parent.document_annotations
    assert db_child.document_annotations.keys() == parent.document_annotations.keys()
    assert list(db_child.document_annotations.values()) == list(parent.document_annotations.values())


# noinspection PyPep8Naming
def test_add_annotation_to_document_surfaceFormLenDiffersFromStartIndicesLen_returnFalse(insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    run_id = run._id
    document_id = list(run.document_annotations.keys())[0]._id
    annotation = Annotation('', ('test', 'text'), (0, 7, 13), (4, 11), AnnotationType('annotation-type1'),
                            Annotator('Andreas', [Role('admin')]), run_id, document_id)

    assert not OrbisService().add_annotation_to_document(annotation)


# noinspection PyPep8Naming
def test_add_annotation_to_document_surfaceFormLenDiffersFromEndIndicesLen_returnFalse(insert_test_data_orbis):
    run = OrbisService().get_runs()[0]
    run_id = run._id
    document_id = list(run.document_annotations.keys())[0]._id
    annotation = Annotation('', ('test', 'text'), (0, 7), (4, 11, 18), AnnotationType('annotation-type1'),
                            Annotator('Andreas', [Role('admin')]), run_id, document_id)

    assert not OrbisService().add_annotation_to_document(annotation)


# noinspection PyPep8Naming
def test_add_annotation_to_document_annotationIsMissingDocumentId_returnFalse(insert_test_data_orbis):
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
def test_add_annotation_to_document_annotationIsMissingRunId_returnFalse(insert_test_data_orbis):
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
    assert OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                AnnotationType('annotation_type1'),
                                                                Annotator('Andreas', []), run_id, document_id))
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
def test_add_annotation_types_addAlreadyExistingAnnotation_annotationTypeIsNotInsertedAndNoErrorOccurs(
        clear_test_data_orbis):
    annotation_type = AnnotationType('annotation-type1')
    assert OrbisService().add_annotation_type(annotation_type)
    assert OrbisService().add_annotation_type(annotation_type)
    annotation_types = OrbisService().get_annotation_types()

    assert len(annotation_types) == 1
    assert annotation_types[0].name == 'annotation-type1'


# noinspection PyPep8Naming
def test_add_annotation_types_addSameAnnotationTypeTwiceInOneCall_annotationTypeIsInsertedOnlyOnce(
        clear_test_data_orbis):
    annotation_type = AnnotationType('annotation-type1')
    assert OrbisService().add_annotation_types([annotation_type, annotation_type])
    annotation_types = OrbisService().get_annotation_types()

    assert len(annotation_types) == 1
    assert annotation_types[0].name == 'annotation-type1'


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

# TODO, anf 06.12.2022: test whether entries are deleted when there are no more references to it
#  ex.: Document contains Annotation, this Annotation is changed and save -> in fact a new Annotation is created,
#  but the old one must be deleted if no other Document references this Annotation
#  (but it must not be deleted if another Document still references it)
