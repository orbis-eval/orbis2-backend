from typing import Dict, List, NamedTuple

from orbis2.model.annotation import Annotation
from orbis2.model.document import Document


class AbstractMetric:

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
