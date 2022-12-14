import logging.config
import os
from datetime import datetime
from pathlib import Path

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.entities.role_dao import RoleDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from src.orbis2.config.app_config import AppConfig
from src.orbis2.database.orbis.orbis_db import OrbisDb


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
