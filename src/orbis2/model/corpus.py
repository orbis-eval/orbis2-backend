from dataclasses import dataclass
from typing import List

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.base_model import BaseModel


@dataclass
class Corpus(BaseModel):
    name: str
    supported_annotation_types: List[AnnotationType]
    _id: int

    def __init__(self, name: str, supported_annotation_types: List[AnnotationType], _id: int = 0):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.supported_annotation_types = supported_annotation_types

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Corpus):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_corpus_dao(cls, corpus_dao: CorpusDao) -> 'Corpus':
        corpus = cls(corpus_dao.name, AnnotationType.from_annotation_type_daos(corpus_dao.supported_annotation_types))
        return corpus

    @classmethod
    def from_corpus_daos(cls, corpus_daos: [CorpusDao]) -> ['Corpus']:
        return [cls.from_corpus_dao(corpus_dao) for corpus_dao in corpus_daos]

    def to_dao(self) -> CorpusDao:
        return CorpusDao(corpus_id=self.id, name=self.name,
                         supported_annotation_types=AnnotationType.to_annotation_type_daos(
                             self.supported_annotation_types))

    def copy(self) -> 'Corpus':
        return Corpus(self.name, [annotation_type.copy() for annotation_type in self.supported_annotation_types])
