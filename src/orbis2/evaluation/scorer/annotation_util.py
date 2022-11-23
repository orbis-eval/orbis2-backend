from itertools import product
from typing import Union

from orbis2.model.annotation import Annotation

SEGMENT_METADATA_KEY = 'segment'


def overlaps(true, predicted):
    """
    Return:
        True, if the true Annotation overlaps the predicted one.

    Note:
        For a multi-surface Annotation it is sufficient, if one of the surfaces
        overlaps.
    """
    return any((p_end >= t_start and p_start <= t_end
                for (t_start, t_end), (p_start, p_end) in product(
        zip(true.start_indices, true.end_indices),
        zip(predicted.start_indices, predicted.end_indices))))


def contains(true: Annotation, predicted: Annotation) -> bool:
    """
    Return:
         True, if the true Annotation contains the predicted one.

    Note:
        For a multi-surface Annotation it is sufficient, if all parts of the
        Annotation are within one (or multiple) true spans.
    """
    for p_start, p_end in zip(predicted.start_indices, predicted.end_indices):
        if not any((t_start <= p_start and t_end >= p_end
                    for t_start, t_end in zip(true.start_indices,
                                              true.end_indices))):
            return False
    return True


def len_overlap(true: Annotation, predicted: Annotation) -> int:
    """
    Return:
         The length of the overlap between true and predicted.
    """
    return sum((max(0, min(t_end, p_end) - max(t_start, p_start))
                for (t_start, t_end), (p_start, p_end) in product(
        zip(true.start_indices, true.end_indices),
        zip(predicted.start_indices, predicted.end_indices))))


def overlap_percentage(true: Annotation, predicted: Annotation) -> float:
    """
    Return:
        The percentage of overlap between true and predicted
    """
    return len_overlap(true, predicted) / (max(len(true), len(predicted)))


def get_annotation_segment(annotation: Annotation) -> Union[str, None]:
    """
    Return:
        The segment of the given Annotation or None string, if no segment has been specified.
    """
    partitions = [metadata.value for metadata in annotation.metadata if metadata.key == SEGMENT_METADATA_KEY]
    return max(partitions) if partitions else None
