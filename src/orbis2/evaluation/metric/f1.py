from collections import namedtuple
from operator import mul
from typing import Dict, List

from orbis2.evaluation.metric import Metric
from orbis2.evaluation.scorer.annotation_entity_scorer import same_entity
from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document

from sklearn.metrics import f1_score, precision_score, recall_score

F1Result = namedtuple('F1Result', 'mP mR mF1 MP MR MF1')


class F1Perfect(Metric):
    """
    Compute P/R/F1 for the perfect match and same entity setting.
    """

    def __init__(self):
        self._scorer = lambda true, pred: mul(exact_match(
            true, pred), same_entity(true, pred))

    def compute(self, reference: Dict[Document, List[Annotation]], annotator: Dict[Document, List[Annotation]]) -> \
            F1Result:
        """
        Args:
            reference: the gold standard annotations.
            annotator: the predicted annotations provided by the annotator.

        Return:
            The metrics provided by the given Metric and their corresponding values.
        """
        y_true_micro = []
        y_true_macro = []
        for document, annotations in reference.items():

            scoring = self._scorer.score_annotation_list(reference, annotator)
            y_true = (len(scoring.tp) + len(scoring.fn)) * [1] + len(scoring.fp) * [0]
            y_pred = (len(scoring.tp) * [1] + len(scoring.fn) * [0] + len(scoring.fp) * [1])
            return F1Result(p=precision_score(y_true, y_pred),
                            r=recall_score(y_true, y_pred),
                            f1=precision_score(y_true, y_pred))

