from orbis2.evaluation.scorer.annotation_util import overlaps, contains, \
    overlap_percentage
from orbis2.model.annotation import Annotation


def same_entity(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The 1 if both annotations refer to the same entity otherwise 0.
    """
    return 1. if true.key == predicted.key else 0.


def same_type(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The 1 if both annotations refer to the same type otherwise 0.
    """
    return 1. if true.annotation_type == predicted.annotation_type else 0.


def same_type_or_proposed_type(true: Annotation, predicted: Annotation) -> float:
    """
        Return:
            The 1 if both annotations refer to the same type (and proposals suggest the same annotation
            type) otherwise 0.
        """
    if predicted.annotation_type == 'proposal':
        return 1. if true.annotation_type == predicted.key.split('#')[1] else 0.

    return 1. if true.annotation_type == predicted.annotation_type else 0.


def always_true(true: Annotation, predicted: Annotation) -> float:
    """
    Always return True. Used for entity recognition.

    Return:
        Always True.
    """
    return True
