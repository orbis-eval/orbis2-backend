from orbis2.model.annotation import Annotation


def overlap(true, predicted):
    """
    Compute whether two Annotations overlap.

    Return:
        True if predicted overlaps true.
    """
    return predicted.end >= true.start and predicted.start <= true.end
