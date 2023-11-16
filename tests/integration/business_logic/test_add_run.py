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
def test_add_runs_emptyDbExistsAndRunIsCorrectlyInitialized_returnTrue(clear_test_data_orbis):
    """
    Tests that the run is correctly added, even if it contains corpus AnnotationTypes that
    have not yet been used for annotating a document.
    """
    assert OrbisService().add_runs([
        Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                               AnnotationType('annotation-type2')]),
            {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
             [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
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
    corpus = OrbisService().get_corpora()[0]
    annotation_types = list(OrbisService().get_corpus_annotation_types(corpus_id=corpus.identifier))

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

    annotation_types = OrbisService().get_corpus_annotation_types(corpora[0].identifier)
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

    annotation_types = OrbisService().get_corpus_annotation_types(corpora[0].identifier)
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
    corpora = OrbisService().get_corpora()
    annotation_types = list(OrbisService().get_corpus_annotation_types(corpus_id=corpora[0].identifier))

    assert len(annotation_types) == 1
    assert annotation_types[0].name == 'annotation-type1'


# noinspection PyPep8Naming
def test_add_run_runContainsDocumentWithRunIdZero_documentIsAddedToLinkedRunIndependentOfItsId(
        clear_test_data_orbis):
    assert OrbisService().add_run(Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                      {Document('Text, das ist ein Beispiel', run_id=0):
                                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]))]}
                                      ))

    runs = OrbisService().get_runs()

    assert len(runs) == 1
    run_documents = list(runs[0].document_annotations.keys())
    assert len(run_documents) == 1
    assert run_documents[0].run_id == runs[0].identifier
    assert run_documents[0].content == 'Text, das ist ein Beispiel'


# noinspection PyPep8Naming
def test_add_run_runContainsSameAnnotationTwice_annotationIsInsertedOnlyOnceAndNoErrorOccurs(
        clear_test_data_orbis):
    assert OrbisService().add_run(Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                      {Document('Text, das ist ein Beispiel'):
                                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key', 'value')])],
                                       Document('Text, das ist ein anderes Beispiel'):
                                            [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                        Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key', 'value')])]}
                                      ))

    annotations = OrbisService().get_annotations()

    assert len(annotations) == 1


# noinspection PyPep8Naming
def test_add_run_runContainsSameMetadataOnDifferentAnnotations_metadataIsInsertedOnlyOnceAndNoErrorOccurs(
        clear_test_data_orbis):
    assert OrbisService().add_run(Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                      {Document('Text, das ist ein Beispiel'):
                                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key', 'value')])],
                                       Document('Text, das ist ein anderes Beispiel'):
                                            [Annotation('', 'anderes', 18, 25, AnnotationType('annotation-type2'),
                                                        Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key', 'value')])]}
                                      ))

    metadata = OrbisService().get_metadata()

    assert len(metadata) == 1
    assert metadata[0].key == 'key'


# noinspection PyPep8Naming
def test_add_run_runContainsSameTwoMetadataOnDifferentAnnotations_metadataAreInsertedOnlyOnceAndNoErrorOccurs(
        clear_test_data_orbis):
    assert OrbisService().add_run(Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
                                      {Document('Text, das ist ein Beispiel'):
                                           [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                                                       Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key1', 'value1'),
                                                                  Metadata('key2', 'value2')])],
                                       Document('Text, das ist ein anderes Beispiel'):
                                            [Annotation('', 'anderes', 18, 25, AnnotationType('annotation-type2'),
                                                        Annotator('Andreas', [Role('admin')]),
                                                        metadata=[Metadata('key1', 'value1'),
                                                                  Metadata('key2', 'value2')])]}
                                      ))

    metadata = OrbisService().get_metadata()

    assert len(metadata) == 2
    assert metadata[0].key == 'key1'
    assert metadata[1].key == 'key2'


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


