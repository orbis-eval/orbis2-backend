from typing import Union, List

from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.run import Run


class OrbisService:

    def __init__(self):
        """
        CONSTRUCTOR

        """
        self.orbis_db = OrbisDb()

    def get_runs(self) -> List[Run]:
        if runs := self.orbis_db.get_runs():
            return Run.from_run_daos(runs)
        return []

    def get_run_by_name(self, run_name: str) -> Union[Run, None]:
        if run := self.orbis_db.get_run_by_name(run_name):
            return Run.from_run_dao(run)
        return None

    def get_run(self, run_id: int) -> Union[Run, None]:
        if run := self.orbis_db.get_run(run_id):
            return Run.from_run_dao(run)
        return None

    def get_runs_by_corpus_id(self, corpus_id: int) -> List[Run]:
        if runs := self.orbis_db.get_run_by_corpus_id(corpus_id):
            return Run.from_run_daos(runs)
        return []

    def get_documents(self) -> List[Document]:
        if documents := self.orbis_db.get_documents():
            return Document.from_document_daos(documents)
        return []

    def get_documents_of_corpus(self, corpus_id: int) -> List[Document]:
        if documents := self.orbis_db.get_documents_of_corpus(corpus_id):
            return Document.from_document_daos(documents)
        return []

    def get_document(self, document_id: int) -> Union[Document, None]:
        if document := self.orbis_db.get_document(document_id):
            return Document.from_document_dao(document)
        return None

    def get_annotations(self) -> List[Annotation]:
        if annotations := self.orbis_db.get_annotations():
            return Annotation.from_annotation_daos(annotations)
        return []

    def get_corpora(self) -> List[Corpus]:
        if corpora := self.orbis_db.get_corpora():
            return Corpus.from_corpus_daos(corpora)
        return []

    def get_corpus_id(self, corpus_name: str) -> Union[int, None]:
        return self.orbis_db.get_corpus_id(corpus_name)

    def get_annotation_types(self) -> List[AnnotationType]:
        if annotation_types := self.orbis_db.get_annotation_types():
            return AnnotationType.from_annotation_type_daos(annotation_types)
        return []

    def get_metadata(self) -> List[Metadata]:
        if metadata := self.orbis_db.get_metadata():
            return Metadata.from_metadata_daos(metadata)
        return []

    def get_annotators(self) -> List[Annotator]:
        if annotators := self.orbis_db.get_annotators():
            return Annotator.from_annotator_daos(annotators)
        return []

    def add_run(self, run: Run) -> bool:
        if run:
            return self.orbis_db.add_run(run.to_dao())
        return False

    def add_runs(self, runs: [Run]) -> bool:
        if not runs:
            return False
        for run in runs:
            if not self.orbis_db.add_run(run.to_dao()):
                return False
        return True

    def add_annotation_to_document(self, annotation: Annotation) -> bool:
        if annotation:
            return self.orbis_db.add_annotation_to_document(annotation.to_document_annotation_dao())
        return False

    def add_annotation_type(self, annotation_type: AnnotationType) -> bool:
        if annotation_type:
            return self.orbis_db.add_annotation_type(annotation_type.to_dao())
        return False

    def add_annotation_types(self, annotation_types: [AnnotationType]) -> bool:
        if not annotation_types:
            return False
        for annotation_type in annotation_types:
            if not self.add_annotation_type(annotation_type):
                return False
        return True
