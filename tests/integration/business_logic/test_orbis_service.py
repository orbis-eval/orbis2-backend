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
    assert run.run_id == 1
    assert run.name == 'run1'
    assert type(run.corpus) is Corpus
    assert run.corpus.corpus_id == 1111
    assert run.corpus.name == 'Corpus1111'

    assert len(run.corpus.supported_annotation_types) == 1
    supported_annotation_type = run.corpus.supported_annotation_types[0]
    assert type(supported_annotation_type) is AnnotationType
    assert supported_annotation_type.type_id == 11111
    assert supported_annotation_type.name == 'type11111'

    documents = list(run.document_annotations.keys())
    assert len(documents) == 1
    document = documents[0]
    assert type(document) is Document
    assert document.document_id == 11
    assert document.content == 'Text, das ist ein Beispiel'

    assert len(document.metadata) == 1
    metadata = document.metadata[0]
    assert type(metadata) is Metadata
    assert metadata.metadata_id == 1111111
    assert metadata.value == 'value1'
    assert metadata.key == 'key1'

    annotations = list(run.document_annotations[document])
    assert len(annotations) == 1
    annotation = annotations[0]
    assert type(annotation) is Annotation
    assert annotation.annotation_id == 111
    assert annotation.key == 'url'
    assert annotation.surface_forms[0] == 'Text'
    assert annotation.start_indices[0] == 0
    assert annotation.end_indices[0] == 4
    assert type(annotation.annotation_type) is AnnotationType
    assert annotation.annotation_type.type_id == 11111
    assert annotation.annotation_type.name == 'type11111'
    assert type(annotation.annotator) is Annotator
    assert annotation.annotator.annotator_id == 111111
    assert annotation.annotator.name == 'annotator111111'

    assert len(annotation.annotator.roles) == 1
    role = annotation.annotator.roles[0]
    assert role.role_id == 2
    assert role.name == 'role2'

    assert len(annotation.metadata) == 1
    metadata = annotation.metadata[0]
    assert type(metadata) is Metadata
    assert metadata.metadata_id == 1111111
    assert metadata.value == 'value1'
    assert metadata.key == 'key1'


# noinspection PyPep8Naming
def test_get_run_by_name_dbExistsAndContainsRun_getRunWithId1(insert_test_data_orbis):
    run = OrbisService().get_run_by_name('run1')

    assert run
    assert run.run_id == 1


# noinspection PyPep8Naming
def test_add_runs_emptyDbExistsAndRunIsCorrectlyInitialized_returnTrue(clear_test_data_orbis):
    assert OrbisService().add_runs([Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                                           AnnotationType('annotation-tpye2')]),
                                        {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
                                             [Annotation('', 'Text', 0, 4, AnnotationType('annotation_type1'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')])]}
                                        )])


# noinspection PyPep8Naming
def test_add_runs_emptyDbExistsAndRunWithMultipleAnnotationsIsCorrectlyInitialized_returnTrue(
        clear_test_data_orbis):
    assert OrbisService().add_runs([Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                                           AnnotationType('annotation-type2')]),
                                        {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
                                             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')]),
                                              Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')])
                                              ]}
                                        )])


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
def test_add_runs_addMultipleRunsContainingAnnotationsWithSameTypeInOneCall_annotationTypeIsInsertedOnlyOnce(
        clear_test_data_orbis):
    assert OrbisService().add_runs([Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                        {Document('Text, das ist ein Beispiel'):
                                             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                         Annotator('Andreas', [Role('admin')]))]}
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
def test_add_runs_emptyDbExistsAndRunWithMultipleDocumentAnnotationsIsCorrectlyInitialized_returnTrue(
        clear_test_data_orbis):
    # TODO, anf 10.11.2022: values (metadata, annotation_types) should only be inserted once
    assert OrbisService().add_runs([Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                                           AnnotationType('annotation-type2')]),
                                        {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
                                             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')]),
                                              Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')])],
                                         Document('Text2, das ist ein neues Beispiel2',
                                                  metadata=[Metadata('key1', 'value1')]):
                                             [Annotation('', 'Text2', 0, 5, AnnotationType('annotation-type1'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')]),
                                              Annotation('', 'Beispiel2', 25, 34, AnnotationType('annotation-type2'),
                                                         Annotator('Andreas', [Role('admin')]),
                                                         metadata=[Metadata('key1', 'value1'),
                                                                   Metadata('key2', 'value2')])]
                                         }
                                        )])


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

    run_id = db_run.get_run_id()
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

    run_id = db_run.get_run_id()
    document_id = list(db_run.document_annotations.keys())[0].document_id
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

    run_id = db_run.get_run_id()
    document_id = list(db_run.document_annotations.keys())[0].document_id
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

    run_id = db_run.get_run_id()
    document_id = list(db_run.document_annotations.keys())[0].document_id
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
