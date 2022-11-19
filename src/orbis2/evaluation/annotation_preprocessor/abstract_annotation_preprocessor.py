from typing import List

from orbis2.model.annotation import Annotation


class AnnotationPreprocessor:

    def preprocess(self, annotation_list: List[Annotation]) -> List[Annotation]:
        """
        Preprocess the given list of Annotations.

        Args:
            annotation_list: the list of Annotations to preprocess.

        Return:
            The preprocessed list.
        """
        raise NotImplementedError
