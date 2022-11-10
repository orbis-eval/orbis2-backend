from operator import mul
from typing import List, Set

from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match, \
    overlapping_match
from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer import overlaps, Scorer, ScorerResult, \
    AnnotationMatch

PREDICTED = [Annotation(1, 5),
             Annotation(7, 14),
             Annotation(8, 14),
             Annotation(12, 14),
             Annotation(22, 24)]

TRUE = [Annotation(12, 14),
        Annotation(16, 18),
        Annotation(22, 24)]


def _g(matches: List[AnnotationMatch]) -> Set[Annotation]:
    """
    Convert a list of AnnotationMatches to the annotation set required for
    comparison.
    """
    return set((match.true for match in matches))


def test_exact_scorer():
    scorer = Scorer(surface_scorer=exact_match,
                    entity_scorer=lambda x, y: True,
                    scoring_operator=mul)
    result = scorer.score_annotation_list(true_annotations=TRUE,
                                          pred_annotations=PREDICTED)
    print(result)
    assert result.fp == {Annotation(1, 5),
                         Annotation(7, 14),
                         Annotation(8, 14)}
    assert _g(result.tp) == {Annotation(12, 14),
                             Annotation(22, 24)}
    assert result.fn == {Annotation(16, 18)}


def test_overlap_scorer():
    """
    Overlapping _scorer: the first match wins, even if it is not the best one.
    """
    scorer = Scorer(surface_scorer=overlapping_match,
                    entity_scorer=lambda x, y: True,
                    scoring_operator=mul)
    result = scorer.score_annotation_list(true_annotations=TRUE,
                                          pred_annotations=PREDICTED)
    print(result)
    assert result.fp == {Annotation(1, 5),
                         Annotation(7, 14),
                         Annotation(8, 14)}
    assert _g(result.tp) == {Annotation(12, 14),
                             Annotation(22, 24)}
    assert result.fn == {Annotation(16, 18)}
