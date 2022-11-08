from typing import List
from operator import mul
from collections import namedtuple

from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer.annotation_util import overlap

ScorerResult = namedtuple('ScorerResult', 'tp, fn, fp')

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
        tp = []
        fp = []
        fn = []
        true_annotations.sort()
        predicted_annotations.sort()
        current_pred_idx = 0

        # redo logic:
        #  1. create sets of overlapping annotations => match candidates
        #  2. determine sets of matching annotations => improved match cand.
        #  3. remove duplicates, ensuring that we maximize matches
        #  4. move all other annotations either into the fp or fn category (!)





        for true in true_annotations:
            # add all annotations located before for the current 'true'
            # annotation to the list of false positives (fp)
            while current_pred_idx < len(predicted_annotations):
                if not predicted_annotations[current_pred_idx].end < \
                       true.start:
                    break
                else:
                    fp.append(predicted_annotations[current_pred_idx])
                    current_pred_idx += 1

            # assign all overlapping annotations to either tp or fp
            # warning -> this might be too simplistic, since the overlap
            # might be a working match with a later true annotation
            # --
            # alternative: create sets of
            while current_pred_idx < len(predicted_annotations) and  \
                    overlap(true, predicted_annotations[current_pred_idx]):
                pred = predicted_annotations[current_pred_idx]
                current_pred_idx += 1
                if self.scoring_operator(
                        self.surface_matcher.score_annotation(true, pred),
                        self.entity_scorer.score_annotation(true, pred)) > 0:
                    tp.append((pred, true))
                    true = None
                    break
                else:
                    fp.append(pred)

            if true:
                fn.append(true)

        return tp, fp, fn
