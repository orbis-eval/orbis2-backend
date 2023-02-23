from collections import namedtuple
from statistics import mean
from typing import Dict, List
from warnings import warn

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.metric.abstract_metric import AbstractMetric
from orbis2.evaluation.scorer import Scorer
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document

from sklearn.metrics import f1_score, precision_score, recall_score

F1Result = namedtuple('F1Result', 'mP mR mF1 MP MR MF1')


class F1Metric(AbstractMetric):
    """
            Compute P/R/F1 for the perfect match and same entity setting.
    """

    def __init__(self, scorer: Scorer, *annotation_preprocessor: AnnotationPreprocessor):
        """
        Args:
            scorer: the used scorer.
            annotation_preprocessor: an optional function for pre-processing the document annotations.
        """
        self._scorer = scorer
        self._annotation_preprocessor = annotation_preprocessor

    def apply_preprocessor(self, annotations: List[Annotation]) -> List[Annotation]:
        for preprocessor in self._annotation_preprocessor:
            annotations = preprocessor.preprocess(annotations)
        return annotations

    def compute(self, eval_runs: List[Dict[Document, List[Annotation]]]) -> F1Result:
        """
        Args:
            eval_runs: The runs to evaluate. The reference run is always on the first position, the run to evaluate on
                       the second one.

        Return:
            The metrics provided by the given Metric and their corresponding values.
        """
        reference, annotator = eval_runs
        y_true_micro = []
        y_pred_micro = []
        if len(reference) != len(annotator):
            warn(f'Reference corpus size ({len(reference)}) differs from the number of annotated documents '
                 f'({len(annotator)}).')

        f1 = []
        p = []
        r = []
        for document, annotations in reference.items():
            if document in annotator:
                scoring = self._scorer.score_annotation_list(self.apply_preprocessor(annotations),
                                                             self.apply_preprocessor(annotator[document]))
            else:
                warn(f'No annotations for document {document.key} found - ignoring document.')
                continue

            y_true = (len(scoring.tp) + len(scoring.fn)) * [1] + len(scoring.fp) * [0]
            y_pred = (len(scoring.tp) * [1] + len(scoring.fn) * [0] + len(scoring.fp) * [1])
            f1.append(f1_score(y_true, y_pred))
            p.append(precision_score(y_true, y_pred))
            r.append(recall_score(y_true, y_pred))

            y_true_micro += y_true
            y_pred_micro += y_pred

        macro_p = mean(p)
        macro_r = mean(r)
        return F1Result(mP=precision_score(y_true_micro, y_pred_micro),
                        mR=recall_score(y_true_micro, y_pred_micro),
                        mF1=f1_score(y_true_micro, y_pred_micro),
                        MP=macro_p,
                        MR=macro_r,
                        MF1=macro_r * macro_p * 2 / (macro_r + macro_p))
