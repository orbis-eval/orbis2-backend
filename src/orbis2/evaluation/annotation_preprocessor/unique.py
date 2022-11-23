from typing import List, Tuple

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.scorer.annotation_util import get_annotation_segment
from orbis2.model.annotation import Annotation


class UniqueSlotValue(AnnotationPreprocessor):
    """
    Preprocess the annotations to provide a unique list of slot values.
    => all Annotations are normalized to position 0 (since presence rather than position matters for slot filing)
    """

    @staticmethod
    def same_slot_value(first: Annotation, second: Annotation) -> bool:
        """
        Return:
            True if both annotations refer to the same slot value else False.
        """
        return first.key == second.key and get_annotation_segment(first) == get_annotation_segment(second)

    @staticmethod
    def contains_same_slot_value(annotations: List[Annotation], needle: Annotation) -> bool:
        """
        Return:
            True if the given annotation List contains a slot value provided by needle, else False.
        """
        return any((UniqueSlotValue.same_slot_value(annotation, needle) for annotation in annotations))

    @staticmethod
    def normalize_indices(indices: Tuple[int], offset: int) -> Tuple[int]:
        """
        Normalizes the start indices to 0.
        """
        return tuple((i - offset for i in indices))

    def preprocess(self, annotations: List[Annotation]) -> List[Annotation]:
        """
        Return:
            A list of annotations with unique entity/slot mappings.
        """
        result = []
        for annotation in annotations:
            if not UniqueSlotValue.contains_same_slot_value(result, annotation):
                result.append(Annotation(key=annotation.key,
                                         surface_forms=annotation.surface_forms,
                                         start_indices=UniqueSlotValue.normalize_indices(annotation.start_indices,
                                                                                         annotation.start_indices[0]),
                                         end_indices=UniqueSlotValue.normalize_indices(annotation.end_indices,
                                                                                       annotation.start_indices[0]),
                                         annotation_type=annotation.annotation_type,
                                         annotator=annotation.annotator))
        return result
