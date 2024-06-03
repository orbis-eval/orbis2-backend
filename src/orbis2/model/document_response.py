from typing import List

import xxhash
from pydantic import Field

from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.document import Document


class DocumentResponse(OrbisPydanticBaseModel):
    documents: List[Document]
    total_count: int = Field(default=None, alias="totalCount")

    def __hash__(self):
        # Create a hash combining the hashes of the documents and the total count
        h = xxhash.xxh32()
        for doc in self.documents:
            h.update(str(doc.identifier).encode('utf-8'))
            h.update(doc.content.encode('utf-8'))
        h.update(str(self.total_count).encode('utf-8'))
        return h.intdigest()


    def __eq__(self, other):
        if isinstance(other, DocumentResponse):
            return self.documents == other.documents and self.total_count == other.total_count
        return False
