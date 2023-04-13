from dataclasses import dataclass
from typing import Dict, List

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.corpus_supports_annotation_type_relation import \
    corpus_supports_annotation_type_table
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.base_model import BaseModel
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document


@dataclass
class Run(BaseModel):
    name: str
    description: str
    corpus: Corpus
    document_annotations: Dict[Document, List[Annotation]]
    supported_annotation_types: Dict[AnnotationType, int]
    # parents: ['Run']
    _id: int

    def __init__(self, name: str, description: str, corpus: Corpus = None,
                 document_annotations: Dict[Document, List[Annotation]] = None,
                 supported_annotation_types: Dict[AnnotationType, int] = None, parents: ['Run'] = None, _id: int = 0):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.description = description
        self.corpus = corpus
        self.document_annotations = document_annotations if document_annotations else {}
        self.supported_annotation_types = supported_annotation_types if supported_annotation_types else {}
        self.parents = parents if parents else []

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Run):
            return self.__hash__() == other.__hash__()
        return False

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
            supported_annotation_types = corpus_supports_annotation_type_table.select()
        run = cls(run_dao.name,
                  run_dao.description,
                  Corpus.from_corpus_dao(run_dao.corpus) if run_dao.corpus else None,
                  document_annotations,
                  Run.from_run_daos(run_dao.parents))
        return run

    @classmethod
    def from_run_daos(cls, run_daos: [RunDao]) -> ['Run']:
        return [cls.from_run_dao(run_dao) for run_dao in run_daos]

    def to_dao(self) -> RunDao:
        return RunDao(run_id=self._id, name=self.name, description=self.description,
                      run_has_documents=[
                          document.to_run_document_dao(
                              [annotation.to_document_annotation_dao() for annotation in annotations]
                          ) for document, annotations in self.document_annotations.items()
                      ], corpus_id=self.corpus._id, corpus=self.corpus.to_dao(),
                      parents=Run.to_run_daos(self.parents))

    @staticmethod
    def to_run_daos(runs: ['Run']) -> [RunDao]:
        return [run.to_dao() for run in runs]

    def copy(self, new_name: str, new_description: str) -> 'Run':
        parents = [self]
        if self.parents:
            parents = parents.extend(self.parents)
        new_run = Run(new_name, new_description, self.corpus.copy(), parents=parents)
        document_annotations = {
            document.copy(new_run._id): [
                annotation.copy(new_run._id, document._id) for annotation in annotations
            ] for document, annotations in self.document_annotations.items()
        }
        new_run.document_annotations = document_annotations
        return new_run
