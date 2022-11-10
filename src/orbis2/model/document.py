from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.model.annotation import Annotation
from orbis2.model.metadata import Metadata


class Document:

    def __init__(self, content: str, run_id: int = None, metadata: [Metadata] = None, done: bool = False):
        """
        CONSTRUCTOR

        """
        self.document_id = None
        self.content = content
        self.run_id = run_id
        self.metadata = metadata if metadata else []
        self.done = done

    @classmethod
    def from_document_dao(cls, document_dao: DocumentDao, run_id: int, done: bool) -> 'Document':
        document = cls(document_dao.content, run_id, Metadata.from_metadata_daos(document_dao.meta_data), done)
        document.document_id = document_dao.document_id
        return document

    def to_dao(self) -> DocumentDao:
        return DocumentDao(document_id=self.document_id, content=self.content,
                           meta_data=Metadata.to_metadata_daos(self.metadata))
