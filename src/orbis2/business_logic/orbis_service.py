import logging
from typing import Union

from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.model.document import Document
from orbis2.model.run import Run


class OrbisService:

    def __init__(self):
        """
        CONSTRUCTOR

        """
        self.orbis_db = OrbisDb()

    def get_runs(self) -> [Run]:
        runs = []
        if run_daos := self.orbis_db.get_runs():
            for run_dao in run_daos:
                runs.append(Run.from_run_dao(run_dao))
        return runs

    def get_runs_by_corpus_id(self, corpus_id: int) -> [Run]:
        runs = []
        if run_daos := self.orbis_db.get_run_by_corpus_id(corpus_id):
            for run_dao in run_daos:
                runs.append(Run.from_run_dao(run_dao))
        return runs

    def get_corpus_id(self, corpus_name: str) -> Union[int, None]:
        return self.orbis_db.get_corpus_id(corpus_name)

    def add_run(self, run: Run) -> bool:
        if run:
            return self.orbis_db.add_run(run.to_dao())
        return False

    def add_runs(self, runs: [Run]) -> bool:
        if runs:
            return self.orbis_db.add_runs(Run.to_run_daos(runs))
        return False
