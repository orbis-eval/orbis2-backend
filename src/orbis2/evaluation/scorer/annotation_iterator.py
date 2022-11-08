"""
Generators for efficiently providing iterations over lists of annotations.
"""
from typing import List

from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer.annotation_util import overlap


def yield_overlapping(first: List[Annotation], second: List[Annotation]):
    """
    Take two _sorted_ lists of annotations and return the overlapping ones.
    """
    for c1 in first:
        for c2 in second:
            if overlap(c1, c2):
                yield overlap(c1, c2)
            else:
                # skip the list's tail (i.e., no more overlaps are possible)
                if c1.end < c2.start:
                    break
