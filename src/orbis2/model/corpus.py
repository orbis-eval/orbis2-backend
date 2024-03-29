from typing import List

from pydantic import Field
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.corpus_supports_annotation_type_dao import CorpusSupportsAnnotationTypeDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.base_model import OrbisPydanticBaseModel


class Corpus(OrbisPydanticBaseModel):
    name: str
    supported_annotation_types: List[AnnotationType] = Field(default=[], alias="supportedAnnotationTypes")

    def __init__(self, name: str, supported_annotation_types: List[AnnotationType]):
        super().__init__(name=name, supported_annotation_types=supported_annotation_types)

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Corpus):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_corpus_dao(cls, corpus_dao: CorpusDao) -> 'Corpus':
        corpus = cls(name=corpus_dao.name, supported_annotation_types=[
            AnnotationType.from_annotation_type_dao(supported.annotation_type).set(color_id=supported.color_id)
            for supported in corpus_dao.supported_annotation_types])
        return corpus

    @classmethod
    def from_corpus_daos(cls, corpus_daos: [CorpusDao]) -> ['Corpus']:
        return [cls.from_corpus_dao(corpus_dao) for corpus_dao in corpus_daos]

    def to_dao(self) -> CorpusDao:
        c = CorpusDao(corpus_id=self.identifier, name=self.name,
                      supported_annotation_types=[
                          (CorpusSupportsAnnotationTypeDao(corpus_id=self.identifier, annotation_type=an.to_dao())
                           if not an.color_id else CorpusSupportsAnnotationTypeDao(
                              corpus_id=self.identifier, annotation_type=an.to_dao(), color_id=an.color_id))
                          for an in self.supported_annotation_types])
        return c
