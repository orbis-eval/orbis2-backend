from typing import List
from operator import mul

from orbis2.evaluation.scorer.surface_matcher import ScorerResult
from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer.annotation_util import overlap

class Scorer:

    def __init__(self, surface_matcher, entity_scorer, scoring_operator=mul):
        """
        Args:
            surface_matcher: SurfaceMatcher used for scoring the entities'
                surface forms.
            entity_scorer: EntityScorer used for scoring the entity type,
                URL, etc.
            scoring_operator: Function used for combining the results from the
                surface_matcher and entity_scorer.
        """
        self.scorer = lambda true, pred: scoring_operator(surface_matcher(
            true, pred), entity_scorer(true, pred))

    def score_annotation_list(self, true_annotations: List[Annotation],
                              pred_annotations: List[Annotation]) \
            -> ScorerResult:
        """
        Args:
            true_annotations: list of gold standard annotations
            pred_annotations: list of predicted annotations
        """
        result = ScorerResult(tp=set(), fn=set(), fp=set())

        for true in sorted(true_annotations):
            # process head, i.e. detected annotations prior to the next true
            # annotation
            while pred_annotations and pred_annotations[0].end <= true.start:
                p = pred_annotations.pop(0)
                result.fp.add(p)

            # process overlap
            for pred in pred_annotations:
                if pred.start >= true.end:
                    break
                if self.scorer(true, pred):
                    result.tp.add((pred, true))
                    pred_annotations.remove(pred)
                    break

        result.fp = result.fp.union(pred_annotations)
        result.fn = set(true_annotations).difference((tp[1] for tp in result.tp))
        return result
