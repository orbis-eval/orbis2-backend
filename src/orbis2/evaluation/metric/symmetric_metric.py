from typing import Dict, List, NamedTuple

from orbis2.evaluation.metric.abstract_metric import AbstractMetric
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document


class SymmetricMetric(AbstractMetric):
    """
    A symmetric metric, i.e. without a ground truth.

    Used for computing symmetric metrics such as the Inter-Rater-Agreement
    """
    def compute_annotation_vector(self, eval_runs: List[Dict[Document, List[Annotation]]]) -> List[Annotation]:
        """
        Args:
            eval_runs: A list of runs that contain the annotations.

        Return:
             A list of all unique annotations provided by the runs.
        """


    def compute(self, eval_runs: List[Dict[Document, List[Annotation]]]) -> \
            NamedTuple:
        """
        Args:
            eval_runs: A list of runs that contain the annotations. The reference run (if required by the metric), is
                       always on the first position within the list.

        Return:
            The metrics provided by the given Metric and their corresponding values.
        """
        raise NotImplementedError
