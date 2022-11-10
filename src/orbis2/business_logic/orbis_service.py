from orbis2.database.orbis.orbis_db import OrbisDb
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

    def add_runs(self, runs: [Run]) -> bool:
        if runs:
            run_daos = []
            for run in runs:
                run_daos.append(run.to_run_dao())
            return self.orbis_db.add_runs(run_daos)
