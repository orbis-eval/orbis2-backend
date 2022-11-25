from typing import List, Tuple

from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.model.annotation import Annotation


class AnnotationTypeFilter(AnnotationPreprocessor):

    def __init__(self, blacklist: Tuple[str, ...] = None, whitelist: Tuple[str, ...] = None):
        self.blacklist = blacklist
        self.whitelist = whitelist

    def preprocess(self, annotation_list: List[Annotation]) -> List[Annotation]:
        """
        Apply the blacklist and whitelist to the given list of annotations.
        """
        if self.blacklist:
            annotation_list = [annotation for annotation in annotation_list
                               if annotation.annotation_type.name not in self.blacklist]
        if self.whitelist:
            annotation_list = [annotation for annotation in annotation_list
                               if annotation.annotation_type.name in self.whitelist]
        return annotation_list
