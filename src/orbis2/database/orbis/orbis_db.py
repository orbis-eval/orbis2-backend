import logging
from typing import Union, List, Callable, Set

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload

from orbis2.database.orbis.entities.annotation_has_metadata_relation import annotation_has_metadata_table
from orbis2.database.orbis.entities.document_has_metadata_relation import document_has_metadata_table
from orbis2.model.run import Run
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

    def get_run_names_by_corpus_id(self, corpus_id: int) -> Union[List[Run], None]:
        """
        Get all run names with a given corpus_id from database

        Args:
            corpus_id:

        Returns: A list of run names or None if no according run exists in the database
        """
        try:
            results = self.session.query(RunDao.run_id, RunDao.name).where(RunDao.corpus_id == corpus_id).all()
            if len(results) > 0:
                return [RunDao(run_id=result.run_id, name=result.name) for result in results]
            logging.debug(f'There are no run entries with corpus id {corpus_id} in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Run names by corpus id request with corpus id: {corpus_id} failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_run_names(self) -> Union[List[RunDao], None]:
        """
        Get all run names from database

        Returns: A list of all run names or None if no run exists
        """
        try:
            results = self.session.query(RunDao.run_id, RunDao.name).all()
            if len(results) > 0:
                return [RunDao(run_id=result.run_id, name=result.name) for result in results]
            logging.debug('There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All run names request failed.')
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
                lambda: self.session.query(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == RunDao.run_id,
                    RunDao.corpus_id == corpus_id
                ).all(),
                f'Documents for corpus request with corpus id: {corpus_id} failed', False
        ):
            return documents
        logging.debug(f'Documents for corpus with corpus id {corpus_id} has not been found in orbis database.')
        return None

    def get_documents_of_run(self, run_id: int) -> Union[List[DocumentDao], None]:
        """
        Get all documents for a given run from database

        Args:
            run_id: id of the run for which the documents are looked up

        Returns: A list of document objects or None if no document exists for this corpus in the database
        """
        if documents := self.try_catch(
                lambda: self.session.query(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).all(),
                f'Documents for run request with run id: {run_id} failed', False
        ):
            return documents
        logging.debug(f'Documents for run with run id {run_id} has not been found in orbis database.')
        return None

    def get_annotations_of_document_by_run_id(self, run_id: int,
                                              document_id: int) -> Union[List[DocumentHasAnnotationDao], None]:
        """
        Get all annotations for a specific document of a specific run from database

        Args:
            run_id:
            document_id:

        Returns: A list of document annotation objects or None if no according annotation exists in the database
        """
        results = self.try_catch(
            lambda: self.session.query(DocumentHasAnnotationDao).where(
                DocumentHasAnnotationDao.document_id == document_id,
                DocumentHasAnnotationDao.run_id == run_id
            ).all(),
            'Get annotations of document by run id failed',
            [])
        if len(results) > 0:
            return results
        logging.debug(f'There are no annotation entries for run({run_id}) - document({document_id}) combination '
                      f'in orbis database.')
        return None

    def get_annotation_of_document_by_run_id(self, run_id: int,
                                             document_id: int,
                                             annotation_id: int) -> Union[DocumentHasAnnotationDao, None]:
        """
        Get specific annotation by id for a specific document of a specific run from database

        Args:
            run_id:
            document_id:
            annotation_id:

        Returns: A single document annotation object or None if no or multiple annotation exists in the database
        """
        if annotation := self.try_catch(
                lambda: self.session.query(DocumentHasAnnotationDao).where(
                    DocumentHasAnnotationDao.annotation_id == annotation_id,
                    DocumentHasAnnotationDao.document_id == document_id,
                    DocumentHasAnnotationDao.run_id == run_id
                ).first(),
                'Get annotation of document by run id failed', None):
            return annotation
        logging.debug(f'There is no annotation entry (id {annotation_id}) for run({run_id}) - document({document_id}) '
                      f'combination in orbis database.')
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

    def get_annotation(self, annotation_id: int) -> Union[AnnotationDao, None]:
        """
        Get annotation from database.

        Args:
         annotation_id:

        Returns: A single annotation object or None if zero or multiple runs exists in the database
        """
        return self.try_catch(
            lambda: self.session.query(AnnotationDao).get(annotation_id),
            f'Run request with run id: {annotation_id} failed', None)

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

    def get_metadata_by_id(self, metadata_id: int) -> Union[MetadataDao, None]:
        """
        Get metadata from database

        Args:
            metadata_id:

        Returns: A single object of metadata or None if no or multiple metadata exists in the database
        """
        return self.try_catch(lambda: self.session.query(MetadataDao).get(metadata_id),
                              f'No metadata with id: {metadata_id} found in orbis database.', None)

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

    def add_annotation_to_document(self, document_has_annotation: DocumentHasAnnotationDao) -> int:
        """
        Add annotation to an existing document in orbis database.

        Args:
            document_has_annotation:

        Returns: True if it worked, false otherwise
        """
        if self.try_catch(lambda: self.session.merge(document_has_annotation),
                          f'Adding the annotation_document {document_has_annotation} failed.') and self.commit():
            return document_has_annotation.annotation_id
        return 0

    def add_annotation_type(self, annotation_type: AnnotationTypeDao) -> bool:
        """
        Add annotation_type to orbis database.

        Args:
            annotation_type:

        Returns: True if it worked, false otherwise
        """
        return self.try_catch(lambda: self.session.merge(annotation_type),
                              f'Adding annotation type {annotation_type} failed.') and self.commit()

    def metadata_is_orphan(self, metadata_id: int) -> bool:
        """
        Checks if metadata given by its id is an orphan
        (meaning no document nor annotation has a relationship to the metadata)

        Args:
            metadata_id:

        Returns: True if metadata is an orphan, false otherwise
        """
        return (self.session.query(annotation_has_metadata_table).filter_by(metadata_id=metadata_id).count() == 0 and
                self.session.query(document_has_metadata_table).filter_by(metadata_id=metadata_id).count() == 0)

    def annotation_is_orphan(self, annotation_id: int) -> bool:
        """
        Checks if annotation given by its id is an orphan
        (meaning it's not linked to any document)

        Args:
            annotation_id:

        Returns: True if annotation is an orphan, false otherwise
        """
        return self.session.query(DocumentHasAnnotationDao).where(
            DocumentHasAnnotationDao.annotation_id == annotation_id
        ).count() == 0

    def document_is_orphan(self, document_id: int) -> bool:
        """
        Checks if document given by its id is an orphan
        (meaning it's not linked to any corpus, check is done on run level, since every corpus at least contains one
        default run)

        Args:
            document_id:

        Returns: True if document is an orphan, false otherwise
        """
        return self.session.query(RunHasDocumentDao).where(
            RunHasDocumentDao.document_id == document_id
        ).count() == 0

    def run_is_orphan(self, run_id: int) -> bool:
        """
        Checks if run given by its id is an orphan
        (meaning no documnets are linked to it)

        Args:
            run_id:

        Returns: True if run is an orphan, false otherwise
        """
        return self.session.query(RunHasDocumentDao).where(
            RunHasDocumentDao.run_id == run_id
        ).count() == 0

    def remove_metadata(self, metadata_id: int) -> bool:
        """
        Removes metadata from orbis database by its id

        Args:
            metadata_id:

        Returns: True if entry could be removed from orbis database, false otherwise
        """
        if metadata := self.get_metadata_by_id(metadata_id):
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            return (self.try_catch(lambda: not self.session.delete(metadata),
                                   f'Metadata with id {metadata_id} could not be removed from orbis db.')
                    and self.commit())
        return False

    def remove_orphan_metadata(self, metadata: Set[MetadataDao]) -> bool:
        """
        Checks for each item in a given list of metadata if it's an orphan, if yes, the item will be removed

        Args:
            metadata:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        # if no metadata is orphan, this statement is true (since: if all([]) -> True)
        if all([self.remove_metadata(meta_data.metadata_id)
                for meta_data in metadata if self.metadata_is_orphan(meta_data.metadata_id)]):
            return self.commit()
        return False

    def remove_annotation(self, annotation_id: int) -> bool:
        """
        Remove Annotation from database, relationship to its metadata is also removed, if a metadata is then an orphan
        it will be deleted.

        Args:
            annotation_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if annotation := self.get_annotation(annotation_id):
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(annotation),
                               f'Annotation with id {annotation_id} could not be removed from orbis db.')
                    and self.commit()):
                return self.remove_orphan_metadata(annotation.meta_data)
        return False

    def remove_orphan_annotations(self, annotations: Set[AnnotationDao]) -> bool:
        """
        Checks for each item in a given list of annotations if it's an orphan, if yes, the item will be removed

        Args:
            annotations:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all([self.remove_annotation(annotation.annotation_id) for annotation in annotations
                if self.annotation_is_orphan(annotation.annotation_id)]):
            return self.commit()
        return False

    def remove_annotation_from_document(self, document_has_annotation: DocumentHasAnnotationDao) -> bool:
        """
        Delete annotation from an existing document in orbis database, further remove the annotation if it's an orphan.

        Args:
            document_has_annotation:

        Returns: True if it worked, false otherwise
        """
        # 'not' isn't necessary in this scenario, session.query().delete() returns number of deleted row, > 0 -> True
        if (self.try_catch(lambda: self.session.query(DocumentHasAnnotationDao).where(
                DocumentHasAnnotationDao.run_id == document_has_annotation.run_id,
                DocumentHasAnnotationDao.document_id == document_has_annotation.document_id,
                DocumentHasAnnotationDao.annotation_id == document_has_annotation.annotation_id).delete(),
                           f'Removing the annotation_document {document_has_annotation} failed.') and self.commit()):
            if (self.annotation_is_orphan(document_has_annotation.annotation_id)
                    and self.remove_annotation(document_has_annotation.annotation_id)):
                return self.commit()
            return True
        return False

    def remove_document(self, document_id: int) -> bool:
        """
        Remove document from database, relationship to its metadata is also removed, if a metadata is then an orphan
        it will be deleted.

        Args:
            document_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if document := self.get_document(document_id):
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(document),
                               f'Document with id {document_id} could not be removed from orbis db.')
                    and self.commit()):
                return self.remove_orphan_metadata(document.meta_data)
        return False

    def remove_orphan_documents(self, documents: Set[DocumentDao]) -> bool:
        """
        Checks for each item in a given list of documents if it's an orphan, if yes, the item will be removed

        Args:
            documents:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all([self.remove_document(document.document_id) for document in documents
                if self.document_is_orphan(document.document_id)]):
            return self.commit()
        return False

    def remove_document_from_corpus(self, document_id: int, corpus_id: int) -> bool:
        """
        Delete document from an existing corpus in orbis database (meaning that the document is removed from all runs
        of this corpus), further remove the document if it's an orphan.

        Args:
            document_id:
            corpus_id:

        Returns: True if it worked, false otherwise
        """
        runs = set(self.get_run_by_corpus_id(corpus_id))
        documents = {self.get_document(document_id)}
        annotations = {document_annotation.annotation
                       for run in runs
                       for run_document in run.run_has_documents if run_document.document_id == document_id
                       for document_annotation in run_document.document_has_annotations}
        if (self.try_catch(lambda: self.session.query(RunHasDocumentDao).where(
                RunHasDocumentDao.run_id == RunDao.run_id,
                RunDao.corpus_id == corpus_id,
                RunHasDocumentDao.document_id == document_id).delete(synchronize_session='fetch'),
                           f'Removing the document ({document_id}) of corpus ({corpus_id}) failed.') and self.commit()):
            # remove annotation is executed twice (second time in remove run if orphan) but it MUST be executed at this
            # point as well, because an annotation can be orphan even when the run isn't
            return (self.remove_orphan_annotations(annotations)
                    and self.remove_orphan_runs(runs)
                    and self.remove_orphan_documents(documents))
        return False

    def remove_run(self, run_id: int) -> bool:
        """
        Remove run from database, relationship to its documents and to its annotations is also removed,
        if a document or an annotation is then an orphan it will be deleted.

        Args:
            run_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if run := self.get_run(run_id):
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(run),
                               f'Run with id {run_id} could not be removed from orbis db.')
                    and self.commit()):
                return (self.remove_orphan_documents({run_document.document for run_document in run.run_has_documents})
                        and self.remove_orphan_annotations({
                            document_annotation.annotation
                            for run_document in run.run_has_documents
                            for document_annotation in run_document.document_has_annotations})
                        )
        return False

    def remove_orphan_runs(self, runs: Set[RunDao]) -> bool:
        """
        Checks for each item in a given list of runs if it's an orphan, if yes, the item will be removed

        Args:
            runs:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all([self.remove_run(run.run_id) for run in runs
                if self.run_is_orphan(run.run_id)]):
            return self.commit()
        return False

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
