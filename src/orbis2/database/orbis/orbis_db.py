import logging
from typing import Union, List

from orbis2.config.app_config import AppConfig
from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_base import OrbisBase
from orbis2.database.sql_db import SqlDb


class OrbisDb(SqlDb):

    def __init__(self):
        """
        CONSTRUCTOR

        """
        super().__init__(AppConfig.get_orbis_db_url(), OrbisBase)

    # def get_corpora(self) -> Union[List[CorpusDao], None]:
    #     """
    #     Get all corpora from database
    #
    #     Returns: A list of corpus objects or None if no corpus exists in the database
    #     """
    #     results = self.session.query(CorpusDao).all()
    #     if len(results) > 0:
    #         return results
    #     logging.debug('There are no corpus entries in orbis database.')
    #     return None

    def get_runs(self) -> Union[List[RunDao], None]:
        """
        Get all runs from database

        Returns: A list of run objects or None if no run exists in the database
        """
        results = self.session.query(RunDao).all()
        if len(results) > 0:
            return results
        logging.debug('There are no run entries in orbis database.')
        return None

    def get_documents(self) -> Union[List[DocumentDao], None]:
        """
        Get all documents from database

        Returns: A list of document objects or None if no document exists in the database
        """
        results = self.session.query(DocumentDao).all()
        if len(results) > 0:
            return results
        logging.debug('There are no document entries in orbis database.')
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

    def add_annotation(self, annotation: AnnotationDao) -> bool:
        """
        Add annotation to orbis database.

        Args:
            annotation:

        Returns: True if it worked, false otherwise.
        """
        try:
            self.session.add(annotation)
            self.commit()
            return True
        except Exception as e:
            logging.warning(f'During adding the annotation {annotation} '
                            f'the following exception occurred: {e.__str__()}')
            return False

    def add_run(self, run: RunDao) -> bool:
        """
        Add run to orbis database.

        Args:
            run:

        Returns: True if it worked, false otherwise.
        """
        try:
            self.session.add(run)
            self.commit()
            return True
        except Exception as e:
            logging.warning(f'During adding the run {run} '
                            f'the following exception occurred: {e.__str__()}')
            return False

    def add_document_has_annotation(self, document_has_annotation: DocumentHasAnnotationDao) -> bool:
        """
        Add document_has_annotation to orbis database.

        Args:
            document_has_annotation:

        Returns: True if it worked, false otherwise.
        """
        try:
            self.session.add(document_has_annotation)
            self.commit()
            return True
        except Exception as e:
            logging.warning(f'During adding the document_has_annotation {document_has_annotation} '
                            f'the following exception occurred: {e.__str__()}')
            return False
