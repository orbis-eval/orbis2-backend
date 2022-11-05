from typing import List
from operator import mul

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
        self.surface_matcher = surface_matcher
        self.entity_scorer = entity_scorer
        self.scoring_operator = scoring_operator

    def score_annotation_list(self, true_annotations: List[Annotation],
                              predicted_annotations: List[Annotation]) -> List:
        # TODO: correctly align annotations prior to scoring (!)
        #       and ensure that we do not score annotations multiple times.
        tp = []
        fp = []
        fn = []
        true_annotations.sort()
        predicted_annotations.sort()
        current_pred_idx = 0
        for true in true_annotations:
            matched = False
            # add all annotations that are aligned for the current 'true'
            # annotation to the list of false positives (fp)
            while current_pred_idx < len(predicted_annotations):
                if not predicted_annotations[current_pred_idx].end < \
                       true.start:
                    break
                else:
                    fp.append(predicted_annotations[current_pred_idx])
                    current_pred_idx += 1

            while current_pred_idx < len(predicted_annotations) and  \
                    overlap(true, predicted_annotations[current_pred_idx]):
                pred = predicted_annotations[current_pred_idx]
                if self.scoring_operator(
                        self.surface_matcher.score_annotation(true, pred),
                        self.entity_scorer.score_annotation(true, pred)) > 0:
                    tp.append(pred)
                    matched = True
                else:
                    # TODO: handle multiple overlaps (!)
                    fp.append((pred, true))
                current_pred_idx += 1

            if not matched:
                fn.append(true)

        return tp, fp, fn

    def score(self, true_annotations: List, predicted_annotations: List) -> \
            List:
        surface_score = self.surface_matcher(true_annotations,
                                             predicted_annotations)
        entity_score = self.entity_scorer(true_annotations,
                                          predicted_annotations)
        # compute the overall score
        return [self.scoring_operator(s, e) for s, e in zip(surface_score,
                                                       entity_score)]
