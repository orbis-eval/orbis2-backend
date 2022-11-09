from orbis2.evaluation.scorer.annotation_surface_matcher import exact_match, \
    overlapping_match, contained_match
from orbis2.model.annotation import Annotation


def test_perfect_match():
    a1 = Annotation(1, 12)
    a2 = Annotation(1, 12)
    half_left = Annotation(3, 7)
    assert exact_match(a1, a2) == 1.
    assert exact_match(a1, half_left) == 0.

def test_overlap_match():
    """
                0123456789012345
    a1        :      xxxx
    perfect   :      xxxx
    half_left :    xxxx
    half_right:        xxxx
    """
    a1 = Annotation(5, 9)
    perfect = Annotation(5, 9)
    half_left = Annotation(3, 7)
    half_right = Annotation(7, 11)
    larger1 = Annotation(5, 15)
    larger2 = Annotation(0, 10)
    larger3 = Annotation(2, 12)

    assert overlapping_match(a1, perfect) == 1.
    assert overlapping_match(a1, half_left) == 0.5
    assert overlapping_match(a1, half_right) == 0.5
    assert overlapping_match(a1, larger1) == 0.4
    assert overlapping_match(a1, larger2) == 0.4
    assert overlapping_match(a1, larger3) == 0.4

    # symmetric
    assert overlapping_match(larger1, a1) == 0.4
    assert overlapping_match(larger2, a1) == 0.4
    assert overlapping_match(larger3, a1) == 0.4


def test_contained_match():
    a1 = Annotation(5, 9)
    a2 = Annotation(5, 9)
    non_contained1 = Annotation(4, 9)
    non_contained2 = Annotation(5, 10)
    non_contained3 = Annotation(8, 10)
    c1 = Annotation(7, 8)
    c2 = Annotation(6, 9)

    # equal
    assert contained_match(a1, a2) == 1.

    # not contained
    assert contained_match(a1, non_contained1) == 0.
    assert contained_match(a1, non_contained2) == 0.
    assert contained_match(a1, non_contained3) == 0.

    # contained and smaller
    assert contained_match(a1, c1) == 0.25
    assert contained_match(a1, c2) == 0.75
