from orbis2.business_logic.orbis_service import OrbisService
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
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

# TODO, anf 10.11.2022: add test for two runs where one has a parent and check whether the parent got the correct child
#  entry
