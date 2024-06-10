from typing import List, Dict, Optional

from cachetools import cached

from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.database.session import cache
from orbis2.evaluation.helper import get_inter_rater_agreement_result, get_scoring_annotation_level
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_match import AnnotationMatch
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.color_palette import ColorPalette
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.gold_standard import GoldStandard
from orbis2.model.metadata import Metadata
from orbis2.model.run import Run
from orbis2.model.scorer_result import ScorerResult


class OrbisService:

    def __init__(self):
        """
        CONSTRUCTOR

        """
        self.orbis_db = OrbisDb()

    @cached(cache)
    def get_runs(self) -> List[Run]:
        if runs := self.orbis_db.get_runs():
            return Run.from_run_daos(runs)
        return []

    def get_run_by_name(self, run_name: str) -> Optional[Run]:
        if run := self.orbis_db.get_run_by_name(run_name):
            return Run.from_run_dao(run)
        return None

    def get_run(self, run_id: int) -> Optional[Run]:
        if run := self.orbis_db.get_run(run_id):
            return Run.from_run_dao(run)
        return None

    def get_runs_by_corpus_id(self, corpus_id: int) -> List[Run]:
        if runs := self.orbis_db.get_runs_by_corpus_id(corpus_id):
            return Run.from_run_daos(runs)
        return []

    def get_run_names(self, corpus_id: int = None, is_gold_standard: bool = False) -> List[Run]:
        if corpus_id:
            runs = Run.from_run_daos(
                self.orbis_db.get_run_names_by_corpus_id(corpus_id, is_gold_standard=is_gold_standard))
        else:
            runs = Run.from_run_daos(self.orbis_db.get_run_names(is_gold_standard=is_gold_standard))

        if not is_gold_standard:
            for run in runs:
                run.inter_rater_agreement = get_inter_rater_agreement_result(
                    run.current_gold_standard.document_annotations, run.document_annotations)

        return runs if runs else []

    @cached(cache)
    def get_gold_standard_names(self, corpus_id: int = None) -> List[GoldStandard]:
        run_daos = []
        if corpus_id:
            run_daos = self.orbis_db.get_run_names_by_corpus_id(corpus_id, is_gold_standard=True)
        else:
            run_daos = self.orbis_db.get_run_names(is_gold_standard=True)

        gold_standards = []

        for run_dao in run_daos:
            gold_standard = GoldStandard.from_run_dao(run_dao)
            gold_standard.number_of_runs = self.orbis_db.count_runs_in_gold_standard(run_dao.run_id)
            gold_standard.number_of_documents = self.count_documents_in_run(run_dao.run_id)
            gold_standards.append(gold_standard)

        return gold_standards if gold_standards else []

    def get_documents(self) -> List[Document]:
        if documents := self.orbis_db.get_documents():
            return Document.from_document_daos(documents)
        return []

    @cached(cache)
    def search_documents(self, search, page_size, skip) -> [List[Document], int]:
        if search:
            documents, total_count = self.orbis_db.search_documents(search, page_size, skip)
            if documents:
                return Document.from_document_daos(documents), total_count
        return [], 0

    @cached(cache)
    def get_documents_of_corpus(self, corpus_id: int, page_size: int = None, skip: int = 0) -> List[Document]:
        if documents := self.orbis_db.get_documents_of_corpus(corpus_id, page_size, skip):
            return Document.from_document_daos(documents)
        return []

    @cached(cache)
    def get_documents_of_run(self,
                             run_id: int,
                             page_size: int = None,
                             skip: int = 0) -> (List[Document], int):
        document_daos = self.orbis_db.get_documents_of_run(run_id, page_size, skip)
        documents = []
        if document_daos:
            documents = Document.from_document_daos(document_daos)

        # Get the total count of documents
        total_count = self.orbis_db.count_documents_in_run(run_id)

        # Get the run by id
        run = self.get_run(run_id)
        if run and run.current_gold_standard:
            for document in documents:
                # Remove all other keys from the document_annotations
                gold_standard_document_annotations = {
                    document: run.current_gold_standard.document_annotations[document]
                }
                run_document_annotations = {
                    document: run.document_annotations[document]
                }
                document.inter_rater_agreement = get_inter_rater_agreement_result(
                    gold_standard_document_annotations,
                    run_document_annotations
                )

        return documents, total_count

    def count_documents_in_run(self, run_id: int) -> int:
        return self.orbis_db.count_documents_in_run(run_id)

    def count_runs_in_gold_standard(self, gold_standard_id: int) -> int:
        return self.orbis_db.count_runs_in_gold_standard(gold_standard_id)

    def map_document_with_scoring(self, run_id: int, document: Document) -> Optional[Document]:
        run = self.get_run(run_id)
        if run and run.current_gold_standard:
            scoring = get_scoring_annotation_level(
                run.current_gold_standard.document_annotations[document],
                run.document_annotations[document]
            )
            document.scoring = ScorerResult(
                tp=[AnnotationMatch(true=match.true, pred=match.pred) for match in scoring.tp],
                fp=scoring.fp,
                fn=scoring.fn,
            )
        return document

    def get_next_document(self, run_id: int, document_id: int) -> Optional[Document]:
        """
        Returns:
            The next document for the given run. Cycles through (i.e., returns the first document when called with the
            last document's document_id).
        """
        doc_obj = None
        if document := self.orbis_db.get_next_document_of_run(run_id, document_id):
            doc_obj = Document.from_document_dao(document)
            doc_obj.run_id = run_id
        return doc_obj

    def get_previous_document(self, run_id: int, document_id: int) -> Optional[Document]:
        """
        Returns:
            The previous document for the given run and document_id. Cycles through (i.e., return the last document
            when called with the first document's document id).
        """
        doc_obj = None
        if document := self.orbis_db.get_previous_document_of_run(run_id, document_id):
            doc_obj = Document.from_document_dao(document)
            doc_obj.run_id = run_id
        return doc_obj

    def get_document(self, run_id: int, document_id: int) -> Optional[Document]:
        doc_obj = None
        if document := self.orbis_db.get_document(document_id):
            doc_obj = Document.from_document_dao(document)
            doc_obj.run_id = run_id
            doc_obj = self.map_document_with_scoring(run_id, doc_obj)
        return doc_obj

    def get_annotations(self, run_id: int = None, document_id: int = None) -> List[Annotation]:
        annotations = []
        if run_id and document_id:
            if document_has_annotations := self.orbis_db.get_annotations_of_document_by_run_id(run_id, document_id):
                annotations = Annotation.from_document_has_annotations(document_has_annotations)

            run = self.orbis_db.get_run(run_id)
            if run and run.current_gold_standard:
                document_has_annotations = self.orbis_db.get_annotations_of_document_by_run_id(
                    run.current_gold_standard.run_id, document_id)
                if document_has_annotations:
                    annotations.extend(Annotation.from_document_has_annotations(document_has_annotations))
        else:
            if annotations := self.orbis_db.get_annotations():
                annotations = Annotation.from_annotation_daos(annotations, run_id, document_id)
        return annotations

    def get_annotation(self, run_id: int, document_id: int, annotation_id: int) -> Optional[Annotation]:
        if run_id and document_id and annotation_id and (
                document_has_annotations := self.orbis_db.get_annotation_of_document_by_run_id(run_id, document_id,
                                                                                               annotation_id)):
            return Annotation.from_document_has_annotation(document_has_annotations)
        return None

    def get_corpora(self) -> List[Corpus]:
        if corpora := self.orbis_db.get_corpora():
            return Corpus.from_corpus_daos(corpora)
        return []

    def get_corpus(self, corpus_id) -> Optional[Corpus]:
        if corpus_id and (corpus := self.orbis_db.get_corpus(corpus_id)):
            return Corpus.from_corpus_dao(corpus)
        return None

    def get_corpus_id(self, corpus_name: str) -> Optional[int]:
        return self.orbis_db.get_corpus_id(corpus_name)

    def get_corpus_annotation_types(self, corpus_id: int) -> Dict[AnnotationType, int]:
        """
        Return a dictionary of all supported AnnotationTypes and their corresponding color_ids.

        Note:
        - the color of an AnnotationType is determined by computing `color_id % len(color_palette)`.
        - the call `set_corpus_annotation_type_color` assigns a different color_id to a corpus AnnotationType.

        Returns:
            A dictionary of all supported AnnotationTypes and their corresponding color_id.
        """
        annotation_types = []
        for annotation_type_dao, color_id in self.orbis_db.get_corpus_annotation_types(corpus_id).items():
            annotation_type = AnnotationType.from_annotation_type_dao(annotation_type_dao)
            annotation_type.color_id = color_id
            annotation_types.append(annotation_type)
        return annotation_types

    def set_corpus_annotation_type_color(self, corpus_id: int, annotation_type_id: int, color_id: int) -> None:
        """
        Set the color id of the given annotation type for a corpus.

        Args:
            corpus_id: the corpus for which the annotation type's color is set.
            annotation_type_id: id of the annotation type
            color_id: id of the color (the effective color to used is computed based on `color_id % len(color_palette)`
        """
        self.orbis_db.set_corpus_annotation_type_color(corpus_id, annotation_type_id, color_id)

    def get_color_palettes(self) -> List[ColorPalette]:
        """
        Returns:
            A list of all available ColorPalettes.
        """
        return self.orbis_db.get_color_palettes()

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
        return all(self.orbis_db.add_run(run.to_dao()) for run in runs)

    def add_annotation_to_document(self, annotation: Annotation) -> Optional[Annotation]:
        if annotation and (annotation_id := self.orbis_db.add_annotation_to_document(
                annotation.to_document_annotation_dao())):
            return self.get_annotation(annotation.run_id, annotation.document_id, annotation_id)
        return None

    def add_annotation_type(self, annotation_type: AnnotationType) -> bool:
        if annotation_type:
            return self.orbis_db.add_annotation_type(annotation_type.to_dao())
        return False

    def add_annotation_types(self, annotation_types: [AnnotationType]) -> bool:
        if not annotation_types:
            return False
        return all(self.add_annotation_type(annotation_type) for annotation_type in annotation_types)

    def delete_annotation_from_document(self, annotation: Annotation) -> bool:
        if annotation:
            return self.orbis_db.delete_annotation_from_document(annotation.to_document_annotation_dao())
        return False

    def delete_document_from_corpus(self, document_id: int, corpus_id: int) -> bool:
        if document_id and corpus_id:
            return self.orbis_db.delete_document_from_corpus(document_id, corpus_id)
        return False

    def delete_corpus(self, corpus_id: int) -> bool:
        if corpus_id:
            return self.orbis_db.delete_corpus(corpus_id)
        return False

    def delete_run(self, run_id: int) -> bool:
        if run_id:
            return self.orbis_db.delete_run(run_id)
        return False
