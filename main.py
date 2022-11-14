import logging.config
from pathlib import Path

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
    metadata = MetadataDao(
        metadata_id=1111111, key='key1', value='value1'
    )
    annotation_type = AnnotationTypeDao(
        type_id=11111, name='type11111'
    )
    run = RunDao(run_id=1, name='run1', description='run1', run_has_documents=[
        RunHasDocumentDao(document=DocumentDao(
            document_id=11, content='Text, das ist ein Beispiel', meta_data=[metadata]
        ), document_has_annotations=[DocumentHasAnnotationDao(
            annotation=AnnotationDao(
                annotation_id=111, key='url', annotation_type=annotation_type,
                annotator=AnnotatorDao(
                    annotator_id=111111, name='annotator111111', roles=[RoleDao(
                        role_id=2, name='role2'
                    )]
                ), meta_data=[metadata], surface_forms=['Text'], start_indices=[0], end_indices=[4]
            )
        )], done=False)
    ], corpus=CorpusDao(corpus_id=1111, name='Corpus1111', supported_annotation_types=[
        annotation_type
    ]))

    orbis_db = OrbisDb()
    print(orbis_db.add_run(run))
    if orbis_db.create_database(True):
        print(orbis_db.add_run(run))
        print(orbis_db.get_runs())
        print(orbis_db.get_documents())
    else:
        print(False)
