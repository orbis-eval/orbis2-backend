from typing import List
from operator import mul


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

    def score(self, true_annotations: List, predicted_annotations: List) -> \
            List:
        surface_score = self.surface_matcher(true_annotations,
                                             predicted_annotations)
        entity_score = self.entity_scorer(true_annotations,
                                          predicted_annotations)
        # compute the overall score
        return [self.scoring_operator(s, e) for s, e in zip(surface_score,
                                                       entity_score)]
