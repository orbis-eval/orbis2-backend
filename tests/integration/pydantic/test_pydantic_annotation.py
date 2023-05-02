from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role


def test_annotation_initialization():
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    assert annotation.surface_forms == ('Text', )
    assert annotation.start_indices == (0, )
    assert annotation.end_indices == (4, )
    assert annotation.annotation_type == AnnotationType('annotation-type1')
    assert annotation.annotator == Annotator('Andreas', [Role('admin')])
    assert annotation.metadata == [Metadata('key1', 'value1'), Metadata('key2', 'value2')]


def test_annotation_json_serialization():
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    assert annotation.json()