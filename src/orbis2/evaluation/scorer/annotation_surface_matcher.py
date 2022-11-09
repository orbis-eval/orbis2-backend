from orbis2.evaluation.scorer.annotation_util import overlap
from orbis2.model.annotation import Annotation


def exact_match(true: Annotation, predicted: Annotation):
    """
    Return:
        The 1 if both annotations match perfectly otherwise 0.
    """
    return 1 if true.start == predicted.start and true.end == true.end \
        else 0


def _overlap_percentage(true: Annotation, predicted: Annotation):
    """
    Return:
        The percentage of overlap between true and predicted
    """
    maxlen = max((true.end - true.start), (predicted.end - predicted.start))
    if true.start <= predicted.start:
        shared = min(true.end, predicted.end) - predicted.start
    else:
        shared = min(true.end, predicted.end) - true.start
    print(shared, maxlen)
    return shared / maxlen

def overlapping_match(true: Annotation, predicted: Annotation):
    """
    Return:
        A number between 0 and 1 with 0 indicating no overlap and 1 a perfect
        match.
    """
    return _overlap_percentage(true, predicted) \
        if overlap(true, predicted) else 0
