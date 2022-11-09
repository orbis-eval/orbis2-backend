from orbis2.model.annotation import Annotation


def overlaps(true, predicted):
    """
    Return:
        True, if the true Annotation overlaps the predicted one.
    """
    return predicted.end >= true.start and predicted.start <= true.end


def contains(true: Annotation, predicted: Annotation) -> bool:
    """
    Return:
         True, if the true Annotation contains the predicted one.
    """
    return true.start <= predicted.start and true.end >= predicted.end
