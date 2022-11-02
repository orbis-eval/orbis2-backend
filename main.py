import logging.config
from pathlib import Path

from src.orbis2.config.app_config import AppConfig
from src.orbis2.database.orbis.orbis_db import OrbisDb


LOGGING_DIR = Path(__file__).parents[0] / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)

if __name__ == '__main__':
    # TODO: anf 02.11.2022: is it correct to add id and then the object again with the id?
    # annotation = AnnotationDao(annotation_id=1, key='', annotation_type_id=11,
    #                            annotation_type=AnnotationTypeDao(type_id=11, name='topic'), annotator_id=111,
    #                            annotator=AnnotatorDao(annotator_id=111, name='Andreas'),
    #                            surface_forms=['text'], start_indices=[0], end_indices=[4])

    # print(OrbisDb().create_database())
    print(OrbisDb().get_annotations())
    # print(OrbisDb().add_annotation(annotation))
