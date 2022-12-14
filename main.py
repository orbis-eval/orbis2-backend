import logging.config
import os
from pathlib import Path

from orbis2.business_logic.orbis_service import OrbisService
from src.orbis2.config.app_config import AppConfig


LOGGING_DIR = Path(__file__).parents[0] / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)

if __name__ == '__main__':


    os.environ['ORBIS_DB_NAME'] = 'orbis_test'
    # OrbisDb().create_database(True)

    corpus_id = OrbisService().get_corpora()[0].id
    documents = OrbisService().get_documents_of_corpus(corpus_id)
    print(documents)
    # start = datetime.now()
    # runs = OrbisService().get_runs()
    # end = datetime.now()
    # logging.info(f'main time: {end - start}')
    # print(runs)
