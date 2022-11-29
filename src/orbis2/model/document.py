from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.model.base_model import BaseModel
from orbis2.model.metadata import Metadata


class Document(BaseModel):

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
        return DocumentDao(document_id=self.get_id(), content=self.content, key=self.key,
                           meta_data=Metadata.to_metadata_daos(self.metadata))

    def to_run_document_dao(self, document_has_annotation_daos: [DocumentHasAnnotationDao] = None) -> RunHasDocumentDao:
        if not document_has_annotation_daos:
            document_has_annotation_daos = []
        return RunHasDocumentDao(run_id=self.run_id, document_id=self.get_id(), document=self.to_dao(),
                                 document_has_annotations=document_has_annotation_daos, done=self.done)
