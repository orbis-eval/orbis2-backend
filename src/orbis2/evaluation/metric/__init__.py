from typing import Dict, List, NamedTuple

from orbis2.model.annotation import Annotation
from orbis2.model.document import Document


class Metric:

    def compute(self, reference: Dict[Document, List[Annotation]], annotator: Dict[Document, List[Annotation]]) -> \
            NamedTuple:
        """
        Args:
            reference: the gold standard annotations.
            annotator: the predicted annotations provided by the annotator.

        Return:
            The metrics provided by the given Metric and their corresponding values.
        """
        raise NotImplementedError
