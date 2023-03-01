from collections import namedtuple
from statistics import mean
from typing import Dict, List
from warnings import warn

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.metric.abstract_metric import AbstractMetric
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document

from statsmodels.stats import inter_rater as irr
from sklearn.metrics import f1_score, precision_score, recall_score

InterRaterAgreementResult = namedtuple('InterRaterAgreement', 'fleiss_kappa_micro fleiss_kappa_macro '
                                                              'average_f1 fleiss_interpretation')


class InterRaterAgreement(AbstractMetric):
    """
    Compute different kinds of inter-rater-agreement between the given runs.

    Note: there are different ways of doing this.
    Compare: https://support.prodi.gy/t/proper-way-to-calculate-inter-annotator-agreement-for-spans-ner/5760/2
    - Kappa: with inter-rater-agreement
    - Average cross-wise F1
    """

    def __init__(self, scorer: SymmetricScorer, *annotation_preprocessor: AnnotationPreprocessor):
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

    def compute(self, eval_runs: List[Dict[Document, List[Annotation]]]) -> InterRaterAgreementResult:
        """
        Args:
            eval_runs: The runs to evaluate. The reference run is always on the first position, the run to evaluate on
                       the second one.

        Return:
            The metrics provided by the given Metric and their corresponding values.
        """
        fleiss_kappa = []
        micro_rater_assessments = []
        for doc in eval_runs[0]:
            rater_assessments = self._scorer.score_annotation_list([self.apply_preprocessor(run[doc])
                                                                    for run in eval_runs])
            micro_rater_assessments.extend(rater_assessments)
            fleiss_kappa.append(irr.fleiss_kappa(irr.aggregate_raters(micro_rater_assessments)))

        return InterRaterAgreementResult(fleiss_kappa_macro=mean(fleiss_kappa),
                                         fleiss_kappa_micro=irr.fleiss_kappa(irr.aggregate_raters(
                                             micro_rater_assessments)))
