from typing import List, Optional

from pydantic import Field
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.metadata import Metadata
from orbis2.model.scorer_result import ScorerResult

from orbis2.evaluation.output_formatter.inter_rater_agreement_result import InterRaterAgreementResult


class Document(OrbisPydanticBaseModel):
    content: str
    key: str
    run_id: int = Field(default=None, alias="runId")
    metadata: List[Metadata] = None
    done: bool = False
    inter_rater_agreement: Optional[InterRaterAgreementResult] = Field(default=None, alias="interRaterAgreement")
    scoring: Optional[ScorerResult] = Field(default=[], alias="scoring")

    def __init__(self, content: str, key: str = '', run_id: int = None, metadata: [Metadata] = None,
                 done: bool = False,
                 inter_rater_agreement: Optional[InterRaterAgreementResult] = None,
                 scoring: Optional[ScorerResult] = None):
        super().__init__(content=content, key=key, run_id=run_id, metadata=metadata, done=done,
                         inter_rater_agreement=inter_rater_agreement,
                         scoring=scoring)
        self.metadata = metadata if metadata else []
        self.scoring = scoring if scoring else []

    def __hash__(self):
        return xxh32_intdigest(self.content + self.key)

    def __eq__(self, other):
        if isinstance(other, Document):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_document_dao(cls, document_dao: DocumentDao, run_id: int = None, done: bool = False) -> 'Document':
        document = cls(content=document_dao.content, key=document_dao.key, run_id=run_id,
                       metadata=Metadata.from_metadata_daos(document_dao.meta_data), done=done)
        return document

    @classmethod
    def from_document_daos(cls, document_daos: [DocumentDao], run_id: int = None, done: bool = False) -> ['Document']:
        return [cls.from_document_dao(document_dao, run_id, done) for document_dao in document_daos]

    def to_dao(self) -> DocumentDao:
        return DocumentDao(document_id=self.identifier, content=self.content, key=self.key,
                           meta_data=Metadata.to_metadata_daos(self.metadata))

    def to_run_document_dao(self, document_has_annotation_daos: [DocumentHasAnnotationDao] = None) -> RunHasDocumentDao:
        if not document_has_annotation_daos:
            document_has_annotation_daos = []
        return RunHasDocumentDao(run_id=self.run_id, document_id=self.identifier, document=self.to_dao(),
                                 document_has_annotations=document_has_annotation_daos, done=self.done)
