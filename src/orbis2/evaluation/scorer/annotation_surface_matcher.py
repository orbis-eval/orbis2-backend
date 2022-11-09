from dataclasses import dataclass
from typing import List, Set

from orbis2.evaluation.scorer.annotation_util import overlap
from orbis2.model.annotation import Annotation


@dataclass
class ScorerResult:
    tp: Set[Annotation]
    fp: Set[Annotation]
    fn: Set[Annotation]

class AbstractSurfaceMatcher:

    def score_annotation(self, true, predicted):
        """
        Args:
            true: the gold standard, true annotation
            predicted: the predicted annotations
        """
        raise NotImplementedError


class PerfectMatcher(AbstractSurfaceMatcher):

    def score_annotation(self, true, predicted):
        return 1 if true.start == predicted.start and true.end == true.end \
            else 0


class OverlappingMatcher(AbstractSurfaceMatcher):

    def score_annotation(self, true, predicted):
        return 1 if overlap(true, predicted) else 0

#
# Unittests
#
