from collections import namedtuple
from dataclasses import dataclass
from itertools import takewhile
from typing import List, Set
from operator import mul

from orbis2.model.annotation import Annotation


class SymmetricScorer:

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
        self._scorer = lambda true, pred: scoring_operator(surface_scorer(
            true, pred), entity_scorer(true, pred))

    def get_unique_annotation_list(self, eval_runs_annotations: List[List[Annotation]]) -> List[Annotation]:
        """
        Return a list of unique annotations that is then used for computing the inter rater agreement.

        Args:
            eval_runs_annotations: The list of annotation lists to score.
        """
        unique_annotation_list = eval_runs_annotations[0][:]
        for eval_run_annotations in eval_runs_annotations[1:]:
            # determine for each current evaluation in of the evaluation run, whether it is already present in the
            # list of unique annotations.
            for current in eval_run_annotations:
                if any((self._scorer(current, other) > 0. for other in unique_annotation_list)):
                    continue
                unique_annotation_list.append(current)

        return unique_annotation_list

    def get_rater_agreement_matrix(self, unique_annotation_list: List[Annotation],
                                   eval_runs_annotations: List[List[Annotation]]) -> List[List[int]]:
        agreement_matrix = []
        # determine for each annotation in the unique_annotation_list the annotators (i.e., runs) that
        # agree with the annotation.
        for current in unique_annotation_list:
            agreement_matrix.append([
                1 if any(self._scorer(current, other) > 0. for other in run_annotation) else 0
                for run_annotation in eval_runs_annotations
            ])
        return agreement_matrix

    def score_annotation_list(self, eval_runs_annotations: List[List[Annotation]]) -> List[Annotation]:
        """
        Compute the evaluation scores based on the evaluation runs' annotations.

        Args:
            eval_runs_annotations: The list of annotation lists to score.

        Return:
            A matrix of rater assessments that can be aggregated with aggregate_raters and then be used
            for computing the Fleiss' Kappa.
        """
        unique_annotation_list = self.get_unique_annotation_list(eval_runs_annotations)
        return self.get_rater_agreement_matrix(unique_annotation_list, eval_runs_annotations)
