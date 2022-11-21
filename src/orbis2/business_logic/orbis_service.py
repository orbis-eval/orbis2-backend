import logging
from typing import Union

from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.run import Run


class OrbisService:

    def __init__(self):
        """
        CONSTRUCTOR

        """
        self.orbis_db = OrbisDb()

    def get_runs(self) -> [Run]:
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

    def get_runs_by_corpus_id(self, corpus_id: int) -> [Run]:
        if runs := self.orbis_db.get_run_by_corpus_id(corpus_id):
            return Run.from_run_daos(runs)
        return []

    def get_corpora(self) -> [Corpus]:
        if corpora := self.orbis_db.get_corpora():
            return Corpus.from_corpus_daos(corpora)
        return []

    def get_corpus_id(self, corpus_name: str) -> Union[int, None]:
        return self.orbis_db.get_corpus_id(corpus_name)

    def get_annotation_types(self) -> [AnnotationType]:
        if annotation_types := self.orbis_db.get_annotation_types():
            return AnnotationType.from_annotation_type_daos(annotation_types)
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
