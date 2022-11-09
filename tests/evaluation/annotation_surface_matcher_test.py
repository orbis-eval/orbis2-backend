from orbis2.evaluation.scorer.annotation_surface_matcher import exact_match, \
    overlapping_match
from orbis2.model.annotation import Annotation


def test_perfect_match():
    a1 = Annotation(1, 12)
    a2 = Annotation(1, 12)
    half_left = Annotation(3, 7)
    assert exact_match(a1, a2) == 1
    assert exact_match(a1, half_left) == 0

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

    assert overlapping_match(a1, perfect) == 1
    assert overlapping_match(a1, half_left) == 0.5
    assert overlapping_match(a1, half_right) == 0.5
    assert overlapping_match(a1, larger1) == 0.4
    assert overlapping_match(a1, larger2) == 0.4
    assert overlapping_match(a1, larger3) == 0.4

    # symetric
    assert overlapping_match(larger1, a1) == 0.4
    assert overlapping_match(larger2, a1) == 0.4
    assert overlapping_match(larger3, a1) == 0.4