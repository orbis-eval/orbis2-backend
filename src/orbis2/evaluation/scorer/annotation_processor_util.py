from typing import List

from orbis2.model.annotation import Annotation


def tokenize(annotations: List[Annotation]) -> List[Annotation]:
    """
    Return:
        A list of annotations that tokenizes the original list.
    """
