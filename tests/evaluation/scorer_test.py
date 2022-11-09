from typing import List

from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer import overlap
from orbis2.evaluation.scorer.surface_matcher import ScorerResult

PREDICTED = [Annotation(1, 5),
             Annotation(7, 14),
             Annotation(8, 14),
             Annotation(12, 14),
             Annotation(22, 24)]

TRUE = [Annotation(12, 14),
        Annotation(16, 18),
        Annotation(22, 24)]


def score_annotation(true_annotations: List[Annotation],
                     pred_annotations: List[Annotation],
                     scorer):
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
            print("POP", p)

        # process overlap
        for pred in pred_annotations:
            if pred.start >= true.end:
                break
            if scorer(true, pred):
                result.tp.add((pred, true))
                pred_annotations.remove(pred)
                break

    result.fp = result.fp.union(pred_annotations)
    result.fn = set(true_annotations).difference((tp[1] for tp in result.tp))
    return result


def exact_scorer(true, pred):
    return true == pred


def overlap_scorer(true, pred):
    return overlap(true, pred)


def test_exact_scorer():
    result: ScorerResult = score_annotation(true_annotations=TRUE,
                                            pred_annotations=PREDICTED,
                                            scorer=exact_scorer)
    print(result)
    assert result.fp == {Annotation(1, 5),
                         Annotation(7, 14),
                         Annotation(8, 14)}
    assert result.tp == {(Annotation(12, 14), Annotation(12, 14)),
                         (Annotation(22, 24), Annotation(22, 24))}
    assert result.fn == {Annotation(16, 18)}
