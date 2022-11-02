import logging
from typing import Union, List

from src.config.app_config import AppConfig
from src.database.orbis.entities.annotation_dao import AnnotationDao
from src.database.orbis.entities.corpus_dao import CorpusDao
from src.database.orbis.orbis_base import OrbisBase
from src.database.sql_db import SqlDb


class OrbisDb(SqlDb):

    def __init__(self):
        """
        CONSTRUCTOR

        """
        super().__init__(AppConfig.get_orbis_db_url(), OrbisBase)

    def get_corpora(self) -> Union[List[CorpusDao], None]:
        """
        Get all corpora from database

        Returns: A list of corpus objects or None if no corpus exists in the database
        """
        results = self.session.query(CorpusDao).all()
        if len(results) > 0:
            return results
        logging.debug('There are no corpus entries in orbis database.')
        return None

    def get_annotations(self) -> Union[List[AnnotationDao], None]:
        """
        Get all annotations from database

        Returns: A list of annotation objects or None if no annotation exists in the database
        """
        results = self.session.query(AnnotationDao).all()
        if len(results) > 0:
            return results
        logging.debug('There are no annotation entries in orbis database.')
        return None
