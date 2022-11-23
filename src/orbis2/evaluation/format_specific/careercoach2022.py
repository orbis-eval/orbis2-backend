from typing import List, Tuple

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.model.annotation import Annotation


def get_type_or_proposed_type(annotation: Annotation) -> str:
    """
    Return:
        The type for the given key.
    """
    return annotation.key.split('#')[1].split("/")[0] if annotation.annotation_type.name == 'proposal' else \
        annotation.annotation_type.name


def same_type_or_proposed_type(true: Annotation, predicted: Annotation) -> float:
    """
        Return:
            The 1 if both annotations refer to the same type (and proposals suggest the same annotation
            type) otherwise 0.
        """
    return 1. if get_type_or_proposed_type(true) == get_type_or_proposed_type(predicted) else 0.


class CareerCoachTypeFilter(AnnotationPreprocessor):

    def __init__(self, blacklist: Tuple[str, ...]):
        self.blacklist = blacklist

    def preprocess(self, annotation_list: List[Annotation]) -> List[Annotation]:
        return [annotation for annotation in annotation_list
                if get_type_or_proposed_type(annotation) not in self.blacklist]
