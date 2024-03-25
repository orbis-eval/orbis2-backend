from typing import Dict, List, Optional
import datetime

from pydantic import Field
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.model.annotation import Annotation
from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.evaluation.metric.inter_rater_agreement import InterRaterAgreement, InterRaterAgreementResult
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer

from operator import mul
from orbis2.evaluation.scorer.annotation_entity_scorer import same_entity
from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match


class Run(OrbisPydanticBaseModel):
    name: str
    description: str = None
    corpus: Corpus = None
    document_annotations: Optional[Dict[Document, List[Annotation]]] = Field(default={}, alias="documentAnnotations")
    parents: Optional[List['Run']] = None
    is_gold_standard: bool = Field(default=False, alias="isGoldStandard")
    inter_rater_agreement: Optional[InterRaterAgreementResult] = Field(default=None, alias="interRaterAgreement")
    created_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now(), alias="createdAt")
    just_created: Optional[bool] = Field(default=False, alias="justCreated")
    current_gold_standard: Optional['Run'] = Field(default=None, alias="currentGoldStandard")

    def __init__(
            self,
            name: str,
            description: str,
            corpus: Corpus = None,
            document_annotations: Dict[Document, List[Annotation]] = None,
            parents: Optional[List['Run']] = None,
            is_gold_standard: bool = False,
            inter_rater_agreement: Optional[InterRaterAgreementResult] = None,
            created_at: Optional[str] = None,
            just_created: Optional[bool] = False,
            current_gold_standard: Optional['Run'] = None
    ):
        super().__init__(
            name=name,
            description=description,
            corpus=corpus,
            document_annotations=document_annotations,
            parents=parents,
            is_gold_standard=is_gold_standard,
            inter_rater_agreement=inter_rater_agreement,
            created_at=datetime.datetime.now() if not created_at else created_at,
            just_created=just_created,
            current_gold_standard=current_gold_standard
        )
        self.document_annotations = self.document_annotations if document_annotations else {}
        self.parents = self.parents if parents else []

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Run):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def get_inter_rater_agreement_result(cls, gold_standard: 'Run', run: 'Run') -> InterRaterAgreementResult:
        scorer = SymmetricScorer(surface_scorer=exact_match, entity_scorer=same_entity, scoring_operator=mul)
        ira = InterRaterAgreement(scorer)
        eval_runs_list = [gold_standard.document_annotations, run.document_annotations]
        if eval_runs_list[0] and eval_runs_list[1]:
            return ira.compute(eval_runs_list)
        return None

    @classmethod
    def from_run_dao(cls, run_dao: RunDao) -> 'Run':
        """
        CONSTRUCTOR

        Args:
            run_dao: run data access object to convert into run

        """
        document_annotations = {}
        for run_document_dao in run_dao.run_has_documents:
            document = Document.from_document_dao(run_document_dao.document, run_dao.run_id, run_document_dao.done)
            document_annotations[document] = Annotation.from_document_has_annotations(
                run_document_dao.document_has_annotations)
        corpus = Corpus.from_corpus_dao(run_dao.corpus) if run_dao.corpus else None
        current_gold_standard = cls.from_run_dao(
            run_dao.current_gold_standard) if run_dao.current_gold_standard else None
        run = cls(name=run_dao.name,
                  description=run_dao.description,
                  corpus=corpus,
                  document_annotations=document_annotations,
                  parents=Run.from_run_daos(run_dao.parents),
                  is_gold_standard=run_dao.is_gold_standard,
                  created_at=run_dao.created_at,
                  current_gold_standard=current_gold_standard)

        return run

    @classmethod
    def from_run_daos(cls, run_daos: [RunDao]) -> ['Run']:
        if not run_daos:
            return []
        return [cls.from_run_dao(run_dao) for run_dao in run_daos]

    def to_dao(self) -> RunDao:
        return RunDao(run_id=self.identifier, name=self.name, description=self.description,
                      run_has_documents=[
                          document.to_run_document_dao(
                              [annotation.to_document_annotation_dao() for annotation in annotations]
                          ) for document, annotations in self.document_annotations.items()
                      ], corpus_id=self.corpus.identifier, corpus=self.corpus.to_dao(),
                      parents=Run.to_run_daos(self.parents),
                      is_gold_standard=self.is_gold_standard,
                      current_gold_standard_id=self.current_gold_standard.identifier
                      if self.current_gold_standard else None)

    @staticmethod
    def to_run_daos(runs: ['Run']) -> [RunDao]:
        return [run.to_dao() for run in runs]

    def copy(self, new_name: str, new_description: str) -> 'Run':
        parents = [self]
        if self.parents:
            parents = parents.extend(self.parents)
        new_run = Run(new_name, new_description, self.corpus.copy(), parents=parents)
        document_annotations = {
            document.refined_copy(run_id=new_run.identifier): [
                annotation.refined_copy(run_id=new_run.identifier, document_id=document.identifier) for annotation in
                annotations
            ] for document, annotations in self.document_annotations.items()
        }
        new_run.document_annotations = document_annotations
        return new_run
