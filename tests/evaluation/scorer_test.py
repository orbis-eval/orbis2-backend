from operator import mul

from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer import overlap, Scorer
from orbis2.evaluation.scorer.surface_matcher import ScorerResult

PREDICTED = [Annotation(1, 5),
             Annotation(7, 14),
             Annotation(8, 14),
             Annotation(12, 14),
             Annotation(22, 24)]

TRUE = [Annotation(12, 14),
        Annotation(16, 18),
        Annotation(22, 24)]


def exact_annotation_scorer(true, pred):
    return true == pred


def overlap_annotation_scorer(true, pred):
    return overlap(true, pred)


def test_exact_scorer():
    scorer = Scorer(surface_matcher=exact_annotation_scorer,
                    entity_scorer=lambda x, y: True,
                    scoring_operator=mul)
    result = scorer.score_annotation_list(true_annotations=TRUE,
                                          pred_annotations=PREDICTED)
    print(result)
    assert result.fp == {Annotation(1, 5),
                         Annotation(7, 14),
                         Annotation(8, 14)}
    assert result.tp == {(Annotation(12, 14), Annotation(12, 14)),
                         (Annotation(22, 24), Annotation(22, 24))}
    assert result.fn == {Annotation(16, 18)}
