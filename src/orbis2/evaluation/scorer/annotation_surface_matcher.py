from orbis2.evaluation.scorer.annotation_util import overlaps, contains, \
    _overlap_percentage
from orbis2.model.annotation import Annotation


def exact_match(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The 1 if both annotations match perfectly otherwise 0.
    """
    return 1. if true == predicted else 0.


def overlapping_match(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        A number between 0 and 1 with 0 indicating no overlap and 1 a perfect
        match.
    """
    return _overlap_percentage(true, predicted) \
        if overlaps(true, predicted) else 0.


def contained_match(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The overlap between true and predicted, if predicted is within true,
        otherwise 0.
    """
    return _overlap_percentage(true, predicted) \
        if contains(true, predicted) else 0.
