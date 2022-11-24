from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.model.annotation import Annotation
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document


class Run:

    def __init__(self, name: str, description: str, corpus: Corpus,
                 document_annotations: dict[Document, [Annotation]] = None, parents: ['Run'] = None,
                 children: ['Run'] = None):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.description = description
        self.corpus = corpus
        # TODO, anf 16.11.2022: maybe change to dict[document_id, (Document, [Annotation])] ?? for faster access by id
        self.document_annotations = document_annotations if document_annotations else {}
        self.parents = parents if parents else []
        self.children = children if children else []
        self.run_id = self.__hash__()

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
        run_id = run_dao.run_id
        for run_document_dao in run_dao.run_has_documents:
            document = Document.from_document_dao(run_document_dao.document, run_id, run_document_dao.done)
            document_annotations[document] = Annotation.from_document_has_annotations(
                run_document_dao.document_has_annotations)
        run = cls(run_dao.name, run_dao.description, Corpus.from_corpus_dao(run_dao.corpus), document_annotations,
                  Run.from_run_daos(run_dao.parents), Run.from_run_daos(run_dao.children))
        if run_dao.run_id:
            run.run_id = run_dao.run_id
        return run

    @classmethod
    def from_run_daos(cls, run_daos: [RunDao]) -> ['Run']:
        return [cls.from_run_dao(run_dao) for run_dao in run_daos]

    def to_dao(self) -> RunDao:
        run_has_document_daos = []
        for document, annotations in self.document_annotations.items():
            document_has_annotation_daos = [
                DocumentHasAnnotationDao(run_id=self.run_id,
                                         document_id=document.document_id,
                                         annotation_id=annotation.annotation_id,
                                         annotation=annotation.to_dao())
                for annotation in annotations]

            run_has_document_daos.append(RunHasDocumentDao(run_id=self.run_id,
                                                           document_id=document.document_id,
                                                           document=document.to_dao(),
                                                           document_has_annotations=document_has_annotation_daos,
                                                           done=document.done))

        return RunDao(run_id=self.run_id, name=self.name, description=self.description,
                      run_has_documents=run_has_document_daos, corpus=self.corpus.to_dao(),
                      parents=Run.to_run_daos(self.parents))

    @staticmethod
    def to_run_daos(runs: ['Run']) -> [RunDao]:
        return [run.to_dao() for run in runs]
