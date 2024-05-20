from typing import Optional

from pydantic import Field

from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.annotation import Annotation


class AnnotationMatch(OrbisPydanticBaseModel):
    true: Optional[Annotation] = Field(default=None)
    pred: Optional[Annotation] = Field(default=None)

    def __init__(self,
                 true: Optional[Annotation] = None,
                 pred: Optional[Annotation] = None):
        super().__init__(true=true, pred=pred)
        self.true = self.true if self.true else []
        self.pred = self.pred if self.pred else []

    def __hash__(self):
        return 1

    def __eq__(self, other):
        if isinstance(other, AnnotationMatch):
            return self.__hash__() == other.__hash__()
        return False
