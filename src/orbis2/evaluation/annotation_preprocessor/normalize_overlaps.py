from typing import List, Tuple

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.corpus_import.format.careercoach import get_type_or_proposed_type
from orbis2.evaluation.scorer import overlaps
from orbis2.model.annotation import Annotation


class NormalizeOverlaps(AnnotationPreprocessor):

    def __init__(self, annotation_priority: Tuple[str, ...]):
        self.annotation_priority = annotation_priority

    def has_higher_priority(self, first: Annotation, second: Annotation) -> bool:
        """
        Note:
            Annotations are ranked based on annotation_priority (more important entities are listed first) and length
            (longer entities receive a higher priority).

        Return:
            True, if first is more important than second otherwise False.
        """
        if self.annotation_priority.index(get_type_or_proposed_type(first)) == self.annotation_priority.index(
                get_type_or_proposed_type(second)):
            return len(first) > len(second)
        else:
            return self.annotation_priority.index(get_type_or_proposed_type(first)) < self.annotation_priority.index(
                get_type_or_proposed_type(second))

    def preprocess(self, annotation_list: List[Annotation]) -> List[Annotation]:
        result = []
        if not annotation_list or not self.annotation_priority:
            return annotation_list

        bucket = list(sorted(annotation_list))
        current_annotation = bucket.pop(0)
        while bucket:
            next_annotation = bucket.pop(0)
            # no overlap => continue
            if not overlaps(current_annotation, next_annotation):
                result.append(current_annotation)
                current_annotation = next_annotation
                continue

            # overlap => the stronger wins
            if not self.has_higher_priority(current_annotation, next_annotation):
                current_annotation = next_annotation
        result.append(current_annotation)
        return result
