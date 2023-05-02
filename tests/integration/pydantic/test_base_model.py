from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role


def test_set():
    """
    Test the behavior of the set function
    """
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation = annotation.set(annotator=Annotator('Albert', [Role('admin')]))

    assert annotation.surface_forms == ('Text', )
    assert annotation.start_indices == (0, )
    assert annotation.end_indices == (4, )
    assert annotation.annotation_type == AnnotationType('annotation-type1')
    assert annotation.annotator == Annotator('Albert', [Role('admin')])
    assert annotation.metadata == [Metadata('key1', 'value1'), Metadata('key2', 'value2')]


def test_refined_copy():
    """
    Test the behavior of the refined copy method.
    """
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation_copy = annotation.refined_copy(annotator=Annotator('Albert', [Role('admin')]))
    annotation_copy.metadata.append(Metadata('key3', 'value3'))

    assert annotation.surface_forms == ('Text', )
    assert annotation.start_indices == (0, )
    assert annotation.end_indices == (4, )
    assert annotation.annotation_type == AnnotationType('annotation-type1')
    assert annotation.annotator == Annotator('Andreas', [Role('admin')])
    assert annotation.metadata == [Metadata('key1', 'value1'), Metadata('key2', 'value2')]

    assert annotation_copy.surface_forms == ('Text', )
    assert annotation_copy.start_indices == (0, )
    assert annotation_copy.end_indices == (4, )
    assert annotation_copy.annotation_type == AnnotationType('annotation-type1')
    assert annotation_copy.annotator == Annotator('Albert', [Role('admin')])
    assert annotation_copy.metadata == [Metadata('key1', 'value1'), Metadata('key2', 'value2'),
                                        Metadata('key3', 'value3')]


def test_str():
    """
    Tests the behavior of the __str__ function.
    """
    annotation_type = AnnotationType('mytype')
    assert str(annotation_type) == '<AnnotationType(color_id=None, name=mytype, _id=4102450537)>'


def test_repr():
    """
    Tests the behavior of the __repr__ function.
    """
    annotation_type = AnnotationType('mytype')
    assert str(annotation_type) == repr(annotation_type)


