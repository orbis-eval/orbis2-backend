from dataclasses import dataclass
from typing import Dict, List, Union

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.corpus_dao import CorpusDao, CorpusSupportsAnnotationTypeDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.base_model import BaseModel


@dataclass
class Corpus(BaseModel):
    name: str
    supported_annotation_types: Dict[AnnotationType, int]
    _id: int

    def __init__(self, name: str, supported_annotation_types: Union[Dict[AnnotationType, int], List[AnnotationType]],
                 _id: int = 0):
        """
        CONSTRUCTOR

        """
        self.name = name
        if isinstance(supported_annotation_types, dict):
            self.supported_annotation_types = supported_annotation_types
        else:
            self.supported_annotation_types = {annotation_type: idx
                                               for idx, annotation_type in enumerate(supported_annotation_types)}

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Corpus):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_corpus_dao(cls, corpus_dao: CorpusDao) -> 'Corpus':
        corpus = cls(corpus_dao.name,
                     {AnnotationType.from_annotation_type_dao(supported.annotation_type): supported.color_id
                      for supported in corpus_dao.supported_annotation_types})
        return corpus

    @classmethod
    def from_corpus_daos(cls, corpus_daos: [CorpusDao]) -> ['Corpus']:
        return [cls.from_corpus_dao(corpus_dao) for corpus_dao in corpus_daos]

    def to_dao(self) -> CorpusDao:
        c = CorpusDao(corpus_id=self._id, name=self.name,
                      supported_annotation_types=[
                             CorpusSupportsAnnotationTypeDao(corpus_id=self._id, annotation_type=an.to_dao(),
                                                             color_id=color)
                             for an, color in self.supported_annotation_types.items()])
        return c

    def copy(self) -> 'Corpus':
        return Corpus(self.name, {annotation_type.copy(): color_id
                                  for annotation_type, color_id in self.supported_annotation_types.items()})
