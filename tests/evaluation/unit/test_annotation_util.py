from orbis2.evaluation.scorer import overlaps
from orbis2.evaluation.scorer.annotation_util import len_overlap
from orbis2.model.annotation import Annotation


def test_overlap():
    """
    Test computation of overlapping annotations.
    """
    true = Annotation(10, 20)
    perfect = Annotation(10, 20)
    none = Annotation(5, 9)
    none2 = Annotation(21, 25)
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

    assert not overlaps(true, none)
    assert not overlaps(true, none2)
    assert not overlaps(none, true)
    assert not overlaps(none2, true)


def test_len_overlap():
    assert len_overlap(Annotation(1, 5), Annotation(3, 5)) == 2
