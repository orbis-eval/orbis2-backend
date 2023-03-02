from collections import namedtuple
from itertools import permutations
from statistics import mean
from typing import Dict, List, Tuple

from statsmodels.stats import inter_rater as irr

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.metric.abstract_metric import AbstractMetric
from orbis2.evaluation.metric.f1 import F1Metric
from orbis2.evaluation.scorer.asymmetric_scorer import AsymmetricScorer
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document

InterRaterAgreementResult = namedtuple('InterRaterAgreement', 'fleiss_kappa_micro fleiss_kappa_macro '
                                                              'average_macro_f1 average_micro_f1 '
                                                              'fleiss_kappa_macro_interpretation '
                                                              'fleiss_kappa_micro_interpretation')


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
        self.scorer = scorer
        self._annotation_preprocessor = annotation_preprocessor

    def apply_preprocessor(self, annotations: List[Annotation]) -> List[Annotation]:
        for preprocessor in self._annotation_preprocessor:
            annotations = preprocessor.preprocess(annotations)
        return annotations

    def compute_average_f1(self, eval_runs: List[Dict[Document, List[Annotation]]]) -> Tuple:
        """
        Compute the average F1 for all raters.

        This is achieved by computing all permutations of the F1 metric and then averaging it.
        Example with 3 raters:
        - F12, F13
        - F21, F23
        - F31, F32

        Return:
            A tuple of macro and micro F1.
        """
        metric = F1Metric(scorer=AsymmetricScorer.from_scorer(self.scorer), *self._annotation_preprocessor)
        reference: Dict[Document, List[Annotation]]
        target: Dict[Document, List[Annotation]]
        f1_results = [metric.compute([reference, target]) for reference, target in permutations(eval_runs, 2)]
        return mean((m.mF1 for m in f1_results)), mean((m.MF1 for m in f1_results))

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
            rater_assessments = self.scorer.score_annotation_list([self.apply_preprocessor(run[doc])
                                                                   for run in eval_runs])
            micro_rater_assessments.extend(rater_assessments)
            fleiss_kappa.append(irr.fleiss_kappa(irr.aggregate_raters(rater_assessments)[0]))

        fleiss_kappa_macro = mean(fleiss_kappa)
        fleiss_kappa_micro = irr.fleiss_kappa(irr.aggregate_raters(micro_rater_assessments)[0])
        average_f1 = self.compute_average_f1(eval_runs)
        return InterRaterAgreementResult(fleiss_kappa_macro=fleiss_kappa_macro,
                                         fleiss_kappa_micro=fleiss_kappa_micro,
                                         average_macro_f1=average_f1[0],
                                         average_micro_f1=average_f1[1],
                                         fleiss_kappa_macro_interpretation=self.interpretation(fleiss_kappa_macro),
                                         fleiss_kappa_micro_interpretation=self.interpretation(fleiss_kappa_micro))

    @staticmethod
    def interpretation(kappa):
        """
        Return:
             the interpretation of the kappa value according to Landis & Koch, 1977.
        """
        if kappa < 0:
            return 'Poor agreement'
        elif kappa <= 0.2:
            return 'Slight agreement'
        elif kappa <= 0.4:
            return 'Fair agreement'
        elif kappa <= 0.6:
            return 'Moderate agreement'
        elif kappa <= 0.8:
            return 'Substantial agreement'
        else:
            return 'Almost perfect agreement'
