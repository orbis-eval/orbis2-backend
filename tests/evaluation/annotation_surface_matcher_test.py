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
    a1 = Annotation(5, 9)
    perfect = Annotation(5, 9)
    half_left = Annotation(3, 7)
    half_right = Annotation(7, 12)

    assert overlapping_match(a1, perfect) == 1
    assert overlapping_match(a1, half_left) == 0.5
    assert overlapping_match(a1, half_right) == 0.5