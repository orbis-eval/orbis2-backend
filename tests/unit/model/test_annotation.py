from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role


# noinspection PyPep8Naming
def test_equals_twoAnnotationsEqualsInAllFields_returnTrue():
    annotation1 = Annotation('key', 'text', 0, 4, AnnotationType('type1'), Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', 'text', 0, 4, AnnotationType('type1'), Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])

    assert annotation1.__eq__(annotation2)


# noinspection PyPep8Naming
def test_equals_twoAnnotationsDifferentInOneSurfaceForm_returnFalse():
    annotation1 = Annotation('key', ('text', 'text2'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', ('text', 'text1'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])

    assert not annotation1.__eq__(annotation2)


# noinspection PyPep8Naming
def test_equals_twoAnnotationsDifferentInOneMetadata_returnFalse():
    annotation1 = Annotation('key', ('text', 'text2'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', ('text', 'text2'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key3', 'value2')])

    assert not annotation1.__eq__(annotation2)


# noinspection PyPep8Naming
def test_equals_twoAnnotationsDifferentInNumberOfMetadata_returnFalse():
    annotation1 = Annotation('key', ('text', 'text2'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', ('text', 'text2'), (0, 5), (4, 10), AnnotationType('type1'),
                             Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1')])

    assert not annotation1.__eq__(annotation2)


# noinspection PyPep8Naming
def test_equals_twoAnnotationsDifferentInAnnotationType_returnFalse():
    annotation1 = Annotation('key', 'text', 0, 4, AnnotationType('type1'), Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', 'text', 0, 4, AnnotationType('type2'), Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])

    assert not annotation1.__eq__(annotation2)


# noinspection PyPep8Naming
def test_equals_twoAnnotationsDifferentInAnnotatorName_returnFalse():
    annotation1 = Annotation('key', 'text', 0, 4, AnnotationType('type1'), Annotator('admin', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation2 = Annotation('key', 'text', 0, 4, AnnotationType('type1'), Annotator('admin2', [Role('admin')]),
                             metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])

    assert not annotation1.__eq__(annotation2)
