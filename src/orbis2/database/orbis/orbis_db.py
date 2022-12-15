import logging
from typing import Union, List, Callable

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload

from orbis2.config.app_config import AppConfig
from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
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
            results = self.session.query(RunDao).options(subqueryload('*')).all()
            if len(results) > 0:
                return results
            logging.debug('There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All runs request failed')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_run_by_name(self, run_name: str) -> Union[RunDao, None]:
        """
        Get run from database by its name

        Returns: A single run object or None if zero or multiple runs exists in the database
        """
        if results := self.try_catch(
            lambda: self.session.query(RunDao).options(subqueryload('*')).where(
                RunDao.name == run_name).all(),
            f'Run request with run name: {run_name} failed', False
        ):
            if len(results) == 1:
                return results[0]
            logging.debug(f'There are {len(results)} (!=0) runs run name {run_name} in orbis database.')
        return None

    def get_run(self, run_id: int) -> Union[RunDao, None]:
        """
        Get run from database by its id

        Returns: A single run object or None if zero or multiple runs exists in the database
        """
        if run := self.try_catch(
            lambda: self.session.query(RunDao).options(subqueryload('*')).get(run_id),
            f'Run request with run id: {run_id} failed', False
        ):
            return run
        logging.debug(f'Run with run id {run_id} has not been found in orbis database.')
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

    def get_document(self, document_id: int) -> Union[DocumentDao, None]:
        """
        Get document from database by its id

        Returns: A single document object or None if zero or multiple documents exists in the database
        """
        if document := self.try_catch(
            lambda: self.session.query(DocumentDao).options(subqueryload('*')).get(document_id),
            f'Document request with document id: {document_id} failed', False
        ):
            return document
        logging.debug(f'Document with document id {document_id} has not been found in orbis database.')
        return None

    def get_run_names_by_corpus_id(self, corpus_id: int) -> Union[List[str], None]:
        """
        Get all runs with a given corpus_id from database

        Args:
            corpus_id:

        Returns: A list of run objects or None if no according run exists in the database
        """
        try:
            results = self.session.query(RunDao.name).where(RunDao.corpus_id == corpus_id).all()
            if len(results) > 0:
                return results
            logging.debug(f'There are no run entries with corpus id {corpus_id} in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Run by corpus id request with corpus id: {corpus_id} failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_run_names(self) -> Union[List[str], None]:
        """
        Get all runs

        Returns: A list of all run objects or None if no run exists
        """
        try:
            results = self.session.query(RunDao.name).all()
            if len(results) > 0:
                return results
            logging.debug(f'There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'all run request failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_corpora(self) -> Union[List[CorpusDao], None]:
        """
        Get all corpora from database

        Returns: A list of corpus objects or None if no according corpus exists in the database
        """
        results = self.try_catch(lambda: self.session.query(CorpusDao).options(subqueryload('*')).all(),
                                 'All corpora request failed',
                                 [])
        if len(results) > 0:
            return results
        logging.debug('There are no corpus entries in orbis database.')
        return None

    def get_corpus_id(self, corpus_name: str) -> Union[int, None]:
        """
        Get the id of a corpus given by its name.

        Args:
            corpus_name:

        Returns: The id if one entry exists, None if zero or more entries exist
        """
        try:
            results = self.session.query(CorpusDao.corpus_id).where(CorpusDao.name == corpus_name).all()
            if len(results) == 1:
                return results[0].corpus_id
            logging.debug(f'{len(results)} (!= 1) corpora found in orbis database.')
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

    def get_documents_of_corpus(self, corpus_id: int) -> Union[List[DocumentDao], None]:
        """
        Get all documents for a given corpus from database

        Args:
            corpus_id: id of the corpus for which the documents are looked up

        Returns: A list of document objects or None if no document exists for this corpus in the database
        """
        if documents := self.try_catch(
                lambda: self.session.query(DocumentDao).where(and_(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == RunDao.run_id,
                    RunDao.corpus_id == corpus_id
                )).all(),
                f'Documents for corpus request with corpus id: {corpus_id} failed', False
        ):
            return documents
        logging.debug(f'Documents for corpus with corpus id {corpus_id} has not been found in orbis database.')
        return None

    def get_annotations(self) -> Union[List[AnnotationDao], None]:
        """
        Get all annotations from database

        Returns: A list of annotation objects or None if no annotation exists in the database
        """
        try:
            results = self.session.query(AnnotationDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no annotation entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All annotations request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_annotation_types(self) -> Union[List[AnnotationTypeDao], None]:
        """
        Get all annotation types from database

        Returns: A list of annotation type objects or None if no annotation type exists in the database
        """
        try:
            results = self.session.query(AnnotationTypeDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no annotation type entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All annotation type request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')

    def get_metadata(self) -> Union[List[MetadataDao], None]:
        """
        Get all metadata from database

        Returns: A list of metadata objects or None if no metadata exists in the database
        """
        try:
            results = self.session.query(MetadataDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no metadata entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All metadata request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')

    def get_annotators(self) -> Union[List[AnnotatorDao], None]:
        """
        Get all annotators from database

        Returns: A list of annotator objects or None if no annotation exists in the database
        """
        try:
            results = self.session.query(AnnotatorDao).all()
            if len(results) > 0:
                return results
            logging.debug('There are no annotator entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All annotator request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def add_run(self, run: RunDao) -> bool:
        """
        Add run to orbis database.

        Args:
            run:

        Returns: True if it worked, false otherwise
        """
        return self.try_catch(lambda: self.session.merge(run), f'Adding the run {run} failed.') and self.commit()

    def add_annotation_to_document(self, document_has_annotation: DocumentHasAnnotationDao) -> bool:
        """
        Add annotation to an existing document in orbis database.

        Args:
            document_has_annotation:

        Returns: True if it worked, false otherwise
        """
        return self.try_catch(lambda: self.session.merge(document_has_annotation),
                              f'Adding the annotation_document {document_has_annotation} failed.') and self.commit()

    def add_annotation_type(self, annotation_type: AnnotationTypeDao) -> bool:
        """
        Add annotation_type to orbis database.

        Args:
            annotation_type:

        Returns: True if it worked, false otherwise
        """
        return self.try_catch(lambda: self.session.merge(annotation_type),
                              f'Adding annotation type {annotation_type} failed.') and self.commit()

    @staticmethod
    def try_catch(method_to_call: Callable[[], any], error_message, default_return_value: any = False) -> any:
        """
        Surround a callable with a try catch block. Log the error_message as warning in case an exception is cached.

        Args:
            method_to_call:
            error_message:
            default_return_value: return this value if exception occurred

        Returns: False if an exception is thrown, otherwise the result of the callable is returned
        """
        try:
            return method_to_call()
        except SQLAlchemyError as e:
            logging.warning(error_message)
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return default_return_value
