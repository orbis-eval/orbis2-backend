import re
from copy import copy
from typing import List

from orbis2.model.annotation import Annotation


RE_TOKENIZE = re.compile(r'\S+')


def tokenize(annotations: List[Annotation]) -> List[Annotation]:
    """
    Return:
        A list of annotations that tokenizes the original list.
    """
    result = []
    for annotation in annotations:
        for surface, start, end in zip(annotation.surface_forms,
                                       annotation.start_indices,
                                       annotation.end_indices):
            idx = 0
            while m := RE_TOKENIZE.search(surface[idx:]):
                new = copy(annotation)
                new.surface_forms = (m.group(), )
                new.start_indices = (start + idx + m.start(), )
                new.end_indices = (start + idx + m.end(), )
                result.append(new)
                idx += m.end()

    return result
