from orbis2.evaluation.scorer.annotation_util import overlaps, contains
from orbis2.model.annotation import Annotation


def exact_match(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The 1 if both annotations match perfectly otherwise 0.
    """
    return 1. if true.start == predicted.start and true.end == true.end \
        else 0.


def _overlap_percentage(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The percentage of overlap between true and predicted
    """
    maxlen = max((true.end - true.start), (predicted.end - predicted.start))
    if true.start <= predicted.start:
        shared = min(true.end, predicted.end) - predicted.start
    else:
        shared = min(true.end, predicted.end) - true.start
    return shared / maxlen


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
