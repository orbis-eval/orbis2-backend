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
    assert run.get_id() > 0
    assert run.name == 'run1'
    assert type(run.corpus) is Corpus
    assert run.corpus.get_id() > 0
    assert run.corpus.name == 'corpus1'

    assert len(run.corpus.supported_annotation_types) == 1
    supported_annotation_type = run.corpus.supported_annotation_types[0]
    assert type(supported_annotation_type) is AnnotationType
    assert supported_annotation_type.get_id() > 0
    assert supported_annotation_type.name == 'annotation-type1'

    documents = list(run.document_annotations.keys())
    assert len(documents) == 1
    document = documents[0]
    assert type(document) is Document
    assert document.get_id() > 0
    assert document.content == 'Text, das ist ein Beispiel'

    assert len(document.metadata) == 1
    metadata = document.metadata[0]
    assert type(metadata) is Metadata
    assert metadata.get_id() > 0
    assert metadata.value == 'value1'
    assert metadata.key == 'key1'

    annotations = list(run.document_annotations[document])
    assert len(annotations) == 1
    annotation = annotations[0]
    assert type(annotation) is Annotation
    assert annotation.get_id() > 0
    assert annotation.key == 'url'
    assert annotation.surface_forms[0] == 'Text'
    assert annotation.start_indices[0] == 0
    assert annotation.end_indices[0] == 4
    assert type(annotation.annotation_type) is AnnotationType
    assert annotation.annotation_type.get_id() > 0
    assert annotation.annotation_type.name == 'annotation-type1'
    assert type(annotation.annotator) is Annotator
    assert annotation.annotator.get_id() > 0
    assert annotation.annotator.name == 'Andreas'

    assert len(annotation.annotator.roles) == 1
    role = annotation.annotator.roles[0]
    assert role.get_id() > 0
    assert role.name == 'admin'

    assert len(annotation.metadata) == 1
    metadata = annotation.metadata[0]
    assert type(metadata) is Metadata
    assert metadata.get_id() > 0
    assert metadata.value == 'value2'
    assert metadata.key == 'key2'


# noinspection PyPep8Naming
def test_get_run_by_name_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    run = OrbisService().get_run_by_name('run1')

    assert run
    assert run.get_id() > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_run_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    run_id = OrbisService().get_runs()[0].get_id()
    run = OrbisService().get_run(run_id)

    assert run
    assert run.get_id() > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_run_by_corpus_id_dbExistsAndContainsRun_returnsRun(insert_test_data_orbis):
    corpus_id = OrbisService().get_corpora()[0].get_id()
    runs = OrbisService().get_runs_by_corpus_id(corpus_id)

    assert runs
    assert len(runs) == 1
    run = runs[0]
    assert run.get_id() > 0
    assert run.name == 'run1'


# noinspection PyPep8Naming
def test_get_corpora_dbExistsAndContainsCorpus_returnsCorpus(insert_test_data_orbis):
    corpora = OrbisService().get_corpora()

    assert corpora
    assert len(corpora) == 1
    corpus = corpora[0]
    assert corpus.get_id() > 0
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
    assert annotation_type.get_id() > 0
    assert annotation_type.name == 'annotation-type1'


# noinspection PyPep8Naming
def test_get_metadata_dbExistsAndContainsMetadata_returnsMetadata(insert_test_data_orbis):
    metadata = OrbisService().get_metadata()

    assert metadata
    assert len(metadata) == 2
    metadatum = metadata[0]
    assert metadatum.get_id() > 0
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


# TODO, anf 29.11.2022: tests checked until here


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
    assert updated_run_on_db.children == run.children


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
    assert updated_run_on_db.children == run.children


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
    assert updated_run_on_db.children == run.children


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
    assert updated_run_on_db.children == run.children


# noinspection PyPep8Naming
def test_add_annotation_to_document_annotationIsMissingDocumentId_returnFalse(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    OrbisService().add_run(run)
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2

    run_id = db_run.get_id()
    assert not OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                    AnnotationType('annotation_type1'),
                                                                    Annotator('Andreas', []), run_id))
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2


# noinspection PyPep8Naming
def test_add_annotation_to_document_annotationIsMissingRunId_returnFalse(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    OrbisService().add_run(run)
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2

    run_id = db_run.get_id()
    document_id = list(db_run.document_annotations.keys())[0].get_id()
    assert not OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                    AnnotationType('annotation_type1'),
                                                                    Annotator('Andreas', []), document_id=document_id))
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2


# noinspection PyPep8Naming
def test_add_annotation_to_document_addNewAnnotationToExistingDocument_existingDocumentContainsNewAnnotation(
        clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    OrbisService().add_run(run)
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2

    run_id = db_run.get_id()
    document_id = list(db_run.document_annotations.keys())[0].get_id()
    assert OrbisService().add_annotation_to_document(Annotation('', 'something', 0, 9,
                                                                AnnotationType('annotation_type1'),
                                                                Annotator('Andreas', []), run_id, document_id))
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 3


# noinspection PyPep8Naming
def test_add_annotation_to_document_addNewAnnotationTwice_annotationShouldBeAddedOnlyOnce(clear_test_data_orbis):
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-tpye2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Annotation', 0, 10, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    OrbisService().add_run(run)
    db_run = OrbisService().get_runs()[0]
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 2

    run_id = db_run.get_id()
    document_id = list(db_run.document_annotations.keys())[0].get_id()
    annotation = Annotation('', 'something', 0, 9, AnnotationType('annotation_type1'),
                            Annotator('Andreas', []), run_id, document_id)
    assert OrbisService().add_annotation_to_document(annotation)
    assert OrbisService().add_annotation_to_document(annotation)
    db_run = OrbisService().get_run(run_id)
    # contains only one document
    assert len(list(db_run.document_annotations.keys())) == 1
    assert len(list(db_run.document_annotations.values())[0]) == 3
# TODO, anf 10.11.2022: add test for two runs where one has a parent and check whether the parent got the correct child
#  entry
