from orbis2.evaluation.scorer import overlaps
from orbis2.evaluation.scorer.annotation_util import len_overlap, get_annotation_segment
from orbis2.model.annotation import get_mock_annotation as Annotation
from orbis2.model.metadata import Metadata


# noinspection PyPep8Naming
def test_overlap_twoOverlappingAnnotations_returnsTrue():
    """
    Test computation of overlapping annotations.
    """
    true = Annotation(10, 20)
    perfect = Annotation(10, 20)
    larger = Annotation(9, 21)
    left = Annotation(5, 11)
    right = Annotation(19, 22)

    assert overlaps(true, perfect)
    assert overlaps(true, larger)
    assert overlaps(true, left)
    assert overlaps(true, right)
    assert overlaps(larger, true)
    assert overlaps(left, true)
    assert overlaps(right, true)


# noinspection PyPep8Naming
def test_overlap_twoNoneOverlappingAnnotations_returnsFalse():
    """
    Test computation of overlapping annotations.
    """
    true = Annotation(10, 20)
    none = Annotation(5, 9)
    none2 = Annotation(21, 25)

    assert not overlaps(true, none)
    assert not overlaps(true, none2)
    assert not overlaps(none, true)
    assert not overlaps(none2, true)


# noinspection PyPep8Naming
def test_len_overlap_twoAnnotations_returnLenOfOverlap():
    """
    01234567890123
     **  *****
       ***   ***
    """
    assert len_overlap(Annotation(1, 5), Annotation(3, 5)) == 2
    assert len_overlap(Annotation(start_indices=(1, 5), end_indices=(3, 10)),
                       Annotation(start_indices=(3, 9), end_indices=(6, 12))) \
           == 1 + 1

def test_get_annotation_segment():
    empty = Annotation(1, 2)
    one_segment = Annotation(1, 2, metadata=(Metadata('segment', 'first')))
    two_segments = Annotation(1, 2, metadata=(Metadata('segment', 'first'), Metadata('segement', 'second')))
    mixed_segment_metadata = Annotation(1, 2, metadata=(Metadata('segment', 'first'),
                                                        Metadata('name', 'Julius'),
                                                        Metadata('segement', 'second')))

    assert get_annotation_segment(empty) is None, "Incorrect handling of Annotation without a segment."
    assert get_annotation_segment(one_segment) == 'first'
    assert get_annotation_segment(two_segments) == 'second', 'Does not return the "largest" segment name.'
    assert get_annotation_segment(mixed_segment_metadata) == 'second', 'Incorrect handling of mixed segment metadata.'