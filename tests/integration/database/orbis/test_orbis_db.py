from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_db import OrbisDb


# noinspection PyPep8Naming
def test_get_runs_get_run_names_by_corpus_id_ExistingDB_CorrectRunDao(insert_test_data_orbis):
    orbis_db = OrbisDb()
    corpora = orbis_db.get_corpora()
    run_list = orbis_db.get_run_names_by_corpus_id(corpora[0].corpus_id)
    assert isinstance(run_list[0], RunDao)
