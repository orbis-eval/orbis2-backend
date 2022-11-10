from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.model.annotation_type import AnnotationType


class Corpus:

    def __init__(self, name: str, supported_annotation_types: [AnnotationType]):
        """
        CONSTRUCTOR

        """
        self.corpus_id = None
        self.name = name
        self.supported_annotation_types = supported_annotation_types

    @classmethod
    def from_corpus_dao(cls, corpus_dao: CorpusDao) -> 'Corpus':
        corpus = cls(corpus_dao.name, AnnotationType.from_annotation_type_daos(corpus_dao.supported_annotation_types))
        corpus.corpus_id = corpus_dao.corpus_id
        return corpus

    def to_dao(self) -> CorpusDao:
        return CorpusDao(corpus_id=self.corpus_id, name=self.name,
                         supported_annotation_types=AnnotationType.to_annotation_type_daos(
                             self.supported_annotation_types))
