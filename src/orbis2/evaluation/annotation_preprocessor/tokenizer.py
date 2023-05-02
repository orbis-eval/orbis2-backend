import re
from copy import copy
from enum import Enum
from typing import List

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.model.annotation import Annotation


class TokenizeBy(Enum):
    """Tokenize text into white-spaced separated tokens."""
    WHITESPACE = re.compile(r'\S+')
    """Tokenize text into single characters."""
    CHARACTERS = re.compile(r'.')


class AnnotationTokenizer(AnnotationPreprocessor):

    def __init__(self, tokenize_by: [TokenizeBy]):
        self._tokenize = tokenize_by.value

    def preprocess(self, annotations: List[Annotation]) -> List[Annotation]:
        """
        Return:
            A list of annotations that tokenizes the original list.
        """
        result = []
        for annotation in annotations:
            for surface, start, _ in zip(annotation.surface_forms,
                                         annotation.start_indices,
                                         annotation.end_indices):
                idx = 0
                while m := self._tokenize.search(surface[idx:]):
                    new = annotation.refined_copy(
                        surface_forms=(m.group(),),
                        start_indices=(start + idx + m.start(),),
                        end_indices=(start + idx + m.end(),)
                    )
                    result.append(new)
                    idx += m.end()
        return result
