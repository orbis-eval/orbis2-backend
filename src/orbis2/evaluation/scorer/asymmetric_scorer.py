from collections import namedtuple
from dataclasses import dataclass
from itertools import takewhile
from typing import List, Set
from operator import mul

from orbis2.evaluation.scorer import Scorer
from orbis2.model.annotation import Annotation

AnnotationMatch = namedtuple('AnnotationMatch', 'score true pred')


@dataclass
class ScorerResult:
    tp: Set[AnnotationMatch]
    fp: Set[Annotation]
    fn: Set[Annotation]


class AsymmetricScorer(Scorer):

    def __init__(self, surface_scorer, entity_scorer, scoring_operator=mul):
        """
        Args:
            surface_scorer: SurfaceMatcher used for scoring the entities'
                surface forms.
            entity_scorer: EntityScorer used for scoring the entity type,
                URL, etc.
            scoring_operator: Function used for combining the results from the
                surface_matcher and entity_scorer.
        """
        self.scorer = lambda true, pred: scoring_operator(surface_scorer(true, pred),
                                                          entity_scorer(true, pred))

    @staticmethod
    def from_scorer(s: Scorer):
        """
        Return a SymmetricScorer with the same scoring rules as the provides one.
        """
        sc = AsymmetricScorer(None, None, None)
        sc.scorer = s.scorer
        return sc

    def score_annotation_list(self, true_annotations: List[Annotation],
                              pred_annotations: List[Annotation]) \
            -> ScorerResult:
        """
        Args:
            true_annotations: list of gold standard annotations
            pred_annotations: list of predicted annotations
        """
        result = ScorerResult(tp=set(), fn=set(), fp=set())
        pred_annotations = sorted(pred_annotations)

        for true in sorted(true_annotations):
            # process head, i.e. detected annotations prior to the next true
            # annotation
            while pred_annotations and pred_annotations[0].end_indices <= true.start_indices:
                p = pred_annotations.pop(0)
                result.fp.add(p)

            # compute best match for overlap
            matches = [AnnotationMatch(score=self.scorer(true, pred),
                                       true=true, pred=pred)
                       for pred in takewhile(lambda pred, gold=true: pred.start_indices < gold.end_indices,
                                             pred_annotations)]
            if matches and (match := max(matches)).score > 0:
                result.tp.add(match)
                pred_annotations.remove(match.pred)

        result.fp = result.fp.union(pred_annotations)
        result.fn = set(true_annotations).difference(
            (tp[1] for tp in result.tp))
        return result
