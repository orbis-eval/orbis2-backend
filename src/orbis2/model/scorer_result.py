from typing import List, Optional

from pydantic import Field

from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_match import AnnotationMatch


class ScorerResult(OrbisPydanticBaseModel):
    tp: Optional[List[AnnotationMatch]] = Field(default=None)
    fp: Optional[List[Annotation]] = Field(default=None)
    fn: Optional[List[Annotation]] = Field(default=None)

    def __init__(self,
                 tp: Optional[List[AnnotationMatch]] = None,
                 fp: Optional[List[Annotation]] = None,
                 fn: Optional[List[Annotation]] = None):
        super().__init__(tp=tp, fp=fp, fn=fn)
        self.tp = self.tp if self.tp else []
        self.fp = self.fp if self.fp else []
        self.fn = self.fn if self.fn else []

    def __hash__(self):
        return 1

    def __eq__(self, other):
        if isinstance(other, ScorerResult):
            return self.__hash__() == other.__hash__()
        return False
