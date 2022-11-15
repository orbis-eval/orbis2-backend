import logging
from typing import Union, List, Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import lazyload

from orbis2.config.app_config import AppConfig
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_base import OrbisBase
from orbis2.database.sql_db import SqlDb


class OrbisDb(SqlDb):

    def __init__(self):
        """
        CONSTRUCTOR

        """
        super().__init__(AppConfig.get_orbis_db_url(), OrbisBase)

    def get_runs(self) -> Union[List[RunDao], None]:
        """
        Get all runs from database

        Returns: A list of run objects or None if no run exists in the database
        """
        try:
            results = self.session.query(RunDao).options(lazyload(RunDao.run_has_documents)).all()
            if len(results) > 0:
                return results
            logging.debug('There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All runs request failed')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_run_by_corpus_id(self, corpus_id: int) -> Union[List[RunDao], None]:
        """
        Get all runs with a given corpus_id from database

        Args:
            corpus_id:

        Returns: A list of run objects or None if no according run exists in the database
        """
        try:
            results = self.session.query(RunDao).where(RunDao.corpus_id == corpus_id).all()
            if len(results) > 0:
                return results
            logging.debug(f'There are no run entries with corpus id {corpus_id} in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Run by corpus id request with corpus id: {corpus_id} failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_corpus_id(self, corpus_name: str) -> Union[int, None]:
        try:
            results = self.session.query(CorpusDao.corpus_id).where(CorpusDao.name == corpus_name).all()
            if len(results) == 1:
                return results[0].corpus_id
            logging.debug(f'{len(results)} (!= 1) Corpora found in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Corpus id request with corpus name: {corpus_name} failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_documents(self) -> Union[List[DocumentDao], None]:
        """
        Get all documents from database

        Returns: A list of document objects or None if no document exists in the database
        """
        try:
            results = self.session.query(DocumentDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no document entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All documents request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_annotation_types(self) -> Union[List[AnnotationTypeDao], None]:
        try:
            results = self.session.query(AnnotationTypeDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no annotation type entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All annotation type request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')

    def add_run(self, run: RunDao) -> bool:
        """
        Add run to orbis database.

        Args:
            run:

        Returns: True if it worked, false otherwise.
        """
        return self.try_catch(lambda: self.session.merge(run), f'Adding the run {run} failed.') and self.commit()

    def add_annotation_type(self, annotation_type: AnnotationTypeDao) -> bool:
        """
        Add annotation_type to orbis database.

        Args:
            annotation_type:

        Returns: True if it worked, false otherwise.
        """
        return self.try_catch(lambda: self.session.merge(annotation_type),
                              f'Adding annotation type {annotation_type} failed.') and self.commit()

    @staticmethod
    def try_catch(method_to_call: Callable[[], bool], error_message) -> bool:
        try:
            return method_to_call()
        except SQLAlchemyError as e:
            logging.warning(error_message)
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return False

