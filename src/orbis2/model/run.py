from dataclasses import dataclass
from typing import Dict, List, Tuple

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.model.annotation import Annotation
from orbis2.model.base_model import BaseModel
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document


@dataclass
class Run(BaseModel):
    name: str
    description: str
    corpus: Corpus
    document_annotations: Dict[int, Tuple[Document, List[Annotation]]]
    # parents: ['Run']

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, name: str, description: str, corpus: Corpus,
                 document_annotations: Dict[int, Tuple[Document, List[Annotation]]] = None, parents: ['Run'] = None):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.description = description
        self.corpus = corpus
        # TODO, anf 16.11.2022: maybe change to dict[document_id, (Document, [Annotation])] ?? for faster access by id
        self.document_annotations = document_annotations if document_annotations else {}
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
            document_annotations[document.get_id()] = (document, Annotation.from_document_has_annotations(
                run_document_dao.document_has_annotations))
        run = cls(run_dao.name, run_dao.description, Corpus.from_corpus_dao(run_dao.corpus), document_annotations,
                  Run.from_run_daos(run_dao.parents))
        return run

    @classmethod
    def from_run_daos(cls, run_daos: [RunDao]) -> ['Run']:
        return [cls.from_run_dao(run_dao) for run_dao in run_daos]

    def to_dao(self) -> RunDao:
        return RunDao(run_id=self.get_id(), name=self.name, description=self.description,
                      run_has_documents=[
                          document.to_run_document_dao(
                              [annotation.to_document_annotation_dao() for annotation in annotations]
                          ) for document, annotations in self.document_annotations.values()
                      ], corpus_id=self.corpus.get_id(), corpus=self.corpus.to_dao(),
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
            document.copy(new_run.get_id()): [
                annotation.copy(new_run.get_id(), document.get_id()) for annotation in annotations
            ] for document, annotations in self.document_annotations.values()
        }
        new_run.document_annotations = document_annotations
        return new_run
