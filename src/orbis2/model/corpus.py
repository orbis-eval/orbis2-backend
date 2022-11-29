from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.base_model import BaseModel


class Corpus(BaseModel):

    def __init__(self, name: str, supported_annotation_types: [AnnotationType]):
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
        if corpus_dao.corpus_id:
            corpus.corpus_id = corpus_dao.corpus_id
        return corpus

    @classmethod
    def from_corpus_daos(cls, corpus_daos: [CorpusDao]) -> ['Corpus']:
        return [cls.from_corpus_dao(corpus_dao) for corpus_dao in corpus_daos]

    def to_dao(self) -> CorpusDao:
        return CorpusDao(corpus_id=self.get_id(), name=self.name,
                         supported_annotation_types=AnnotationType.to_annotation_type_daos(
                             self.supported_annotation_types))
