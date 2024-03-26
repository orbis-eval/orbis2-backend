from typing import List, Optional

from pydantic import Field
from xxhash import xxh32_intdigest

from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.annotation import Annotation


class ScorerResult(OrbisPydanticBaseModel):
    tp: Optional[List[Annotation]] = Field(default=None)
    fp: Optional[List[Annotation]] = Field(default=None)
    fn: Optional[List[Annotation]] = Field(default=None)

    def __init__(self,
                 tp: Optional[List[Annotation]] = None,
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
