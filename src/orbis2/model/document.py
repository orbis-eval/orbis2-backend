from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.model.metadata import Metadata


class Document:

    def __init__(self, content: str, key: str = '', run_id: int = None, metadata: [Metadata] = None,
                 done: bool = False):
        """
        CONSTRUCTOR

        """
        self.content = content
        self.key = key
        self.run_id = run_id
        self.metadata = metadata if metadata else []
        self.done = done
        self.document_id = self.__hash__()

    def __hash__(self):
        return xxh32_intdigest(self.content + self.key)

    def __eq__(self, other):
        if isinstance(other, Document):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_document_dao(cls, document_dao: DocumentDao, run_id: int, done: bool) -> 'Document':
        document = cls(document_dao.content, document_dao.key, run_id,
                       Metadata.from_metadata_daos(document_dao.meta_data), done)
        if document_dao.document_id:
            document.document_id = document_dao.document_id
        return document

    def to_dao(self) -> DocumentDao:
        return DocumentDao(document_id=self.document_id, content=self.content, key=self.key,
                           meta_data=Metadata.to_metadata_daos(self.metadata))
