import logging
from typing import List, Callable, Set, Dict, Optional, cast

from sqlalchemy import select, func, and_, cast, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload

from orbis2.config.app_config import AppConfig
from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_has_metadata_relation import annotation_has_metadata_table
from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.color_palette_dao import ColorPaletteDao
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.corpus_supports_annotation_type_dao import CorpusSupportsAnnotationTypeDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import DocumentHasAnnotationDao
from orbis2.database.orbis.entities.document_has_metadata_relation import document_has_metadata_table
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.entities.run_has_document_dao import RunHasDocumentDao
from orbis2.database.orbis.orbis_base import OrbisBase
from orbis2.database.sql_db import SqlDb
from orbis2.model.color_palette import ColorPalette


class OrbisDb(SqlDb):

    def __init__(self):
        """
        CONSTRUCTOR

        """
        super().__init__(AppConfig.get_orbis_db_url(), OrbisBase)

    def get_runs(self) -> Optional[List[RunDao]]:
        """
        Get all runs from database

        Returns: A list of run objects or None if no run exists in the database
        """
        try:
            results = self.session.scalars(select(RunDao).options(subqueryload('*'))).all()
            if len(results) > 0:
                return results
            logging.debug('There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All runs request failed')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_run_by_name(self, run_name: str) -> Optional[RunDao]:
        """
        Get run from database by its name

        Returns: A single run object or None if zero or multiple runs exists in the database
        """
        if results := self.try_catch(
                lambda: self.session.scalars(select(RunDao).options(subqueryload('*')).where(
                    RunDao.name == run_name)).all(),
                f'Run request with run name: {run_name} failed', False
        ):
            if len(results) == 1:
                return results[0]
            logging.debug(f'There are {len(results)} (!=0) runs run name {run_name} in orbis database.')
        return None

    def get_run(self, run_id: int) -> Optional[RunDao]:
        """
        Get run from database by its id

        Returns: A single run object or None if zero or multiple runs exists in the database
        """
        if run := self.try_catch(
                lambda: self.session.get(RunDao, run_id),
                f'Run request with run id: {run_id} failed', False
        ):
            return run
        logging.debug(f'Run with run id {run_id} has not been found in orbis database.')
        return None

    def get_runs_by_corpus_id(self, corpus_id: int, is_gold_standard: bool = False) -> Optional[List[RunDao]]:
        """
        Get all runs with a given corpus_id from database

        Args:
            corpus_id:
            is_gold_standard:

        Returns: A list of run objects or None if no according run exists in the database
        """
        try:
            results = self.session.scalars(select(RunDao).options(subqueryload('*')).where(
                and_(RunDao.corpus_id == corpus_id, RunDao.is_gold_standard == is_gold_standard)
            )).all()
            if len(results) > 0:
                return results
            logging.debug(f'There are no run entries with corpus id {corpus_id} in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Run by corpus id request with corpus id: {corpus_id} failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_corpus(self, corpus_id: int) -> Optional[CorpusDao]:
        """
        Get corpus from database by its id

        Returns: A single corpus object or None if zero or multiple corpora exists in the database
        """
        if corpus := self.try_catch(
                lambda: self.session.scalars(select(CorpusDao).where(CorpusDao.corpus_id == corpus_id)).first(),
                f'Corpus request with corpus id: {corpus_id} failed', False
        ):
            return corpus
        logging.debug(f'Corpus with corpus id {corpus_id} has not been found in orbis database.')
        return None

    def get_document(self, document_id: int) -> Optional[DocumentDao]:
        """
        Get document from database by its id

        Returns: A single document object or None if zero or multiple documents exists in the database
        """
        if document := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).options(subqueryload('*')).where(
                    DocumentDao.document_id == document_id)).first(),
                f'Document request with document id: {document_id} failed', False
        ):
            return document
        logging.debug(f'Document with document id {document_id} has not been found in orbis database.')
        return None

    def get_run_names_by_corpus_id(self, corpus_id: int, is_gold_standard: bool = False) -> Optional[List[RunDao]]:
        """
        Get all run names with a given corpus_id from database.
        If gold standard is true, then filter runs by it as well

        Args:
            corpus_id:
            is_gold_standard:

        Returns: A list of run names or None if no according run exists in the database
        """
        try:
            results = self.session.scalars(select(RunDao).filter(
                and_(RunDao.corpus_id == corpus_id, RunDao.is_gold_standard == is_gold_standard)).order_by(
                RunDao.created_at.desc())).all()
            if len(results) > 0:
                return results
            logging.debug(f'There are no run entries with corpus id {corpus_id} in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Run names by corpus id request with corpus id: {corpus_id} failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_run_names(self, is_gold_standard: bool = False) -> Optional[List[RunDao]]:
        """
        Get all run names from database

        Args:
            is_gold_standard:

        Returns: A list of all run names or None if no run exists
        """
        try:
            results = self.session.scalars(select(RunDao).where(RunDao.is_gold_standard == is_gold_standard).order_by(
                RunDao.created_at.desc())).all()
            if len(results) > 0:
                return results
            logging.debug('There are no run entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All run names request failed.')
            logging.debug(f'the following exception occurred: {e.__str__()}')
            return None

    def get_corpora(self) -> Optional[List[CorpusDao]]:
        """
        Get all corpora from database

        Returns: A list of corpus objects or None if no according corpus exists in the database
        """
        results = self.try_catch(lambda: self.session.scalars(select(CorpusDao).options(subqueryload('*'))).all(),
                                 'All corpora request failed',
                                 [])
        if len(results) > 0:
            return results
        logging.debug('There are no corpus entries in orbis database.')
        return None

    def get_corpus_id(self, corpus_name: str) -> Optional[int]:
        """
        Get the id of a corpus given by its name.

        Args:
            corpus_name:

        Returns: The id if one entry exists, None if zero or more entries exist
        """
        try:
            results = self.session.scalars(select(CorpusDao.corpus_id).where(CorpusDao.name == corpus_name)).all()
            if len(results) == 1:
                return results[0]
            logging.debug(f'{len(results)} (!= 1) corpora found in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning(f'Corpus id request with corpus name: {corpus_name} failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_documents(self) -> Optional[List[DocumentDao]]:
        """
        Get all documents from database

        Returns: A list of document objects or None if no document exists in the database
        """
        try:
            results = self.session.scalars(select(DocumentDao).options(subqueryload('*'))).all()
            if len(results) > 0:
                return results
            logging.debug('There are no document entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All documents request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def search_documents(self,
                         search_query: str,
                         page_size: int = None,
                         skip: int = 0) -> (List[DocumentDao], int):
        """
        Search documents by content, case-insensitively.

        Args:
            search_query: The search term to filter documents by content, case-insensitively.
            page_size: Number of documents per page.
            skip: Number of documents to skip (for pagination).

        Returns:
            A list of document objects or None if no documents are found and the total count of documents.
        """
        try:
            query = (self.session.query(DocumentDao)
                     .filter(
                DocumentDao.content.ilike(f"%{search_query}%") | cast(DocumentDao.document_id, String).like(
                    f"%{search_query}%"))
                     .offset(skip))
            if page_size is not None:
                query = query.limit(page_size)

            documents = query.all()
            print("docs = ", documents)
            total_count = query.count()
            if documents and total_count:
                return documents, total_count
            else:
                logging.debug(f'No documents found for search query: {search_query}')
                return [], 0
        except Exception as e:
            logging.error(f"Search documents request failed: {e}")
            return [], 0

    def get_documents_of_corpus(self,
                                corpus_id: int,
                                page_size: int = None,
                                skip: int = 0) -> (Optional[List[DocumentDao]], int):
        """
        Get all documents for a given corpus from database

        Args:
            corpus_id: id of the corpus for which the documents are looked up
            page_size: defines how many documents should be loaded, if None all documents are loaded
            skip: defines how many documents should be skipped

        Returns: A tuple containing a list of document objects and the total count of documents
        """
        try:
            query = self.session.query(DocumentDao).join(
                RunHasDocumentDao, DocumentDao.document_id == RunHasDocumentDao.document_id
            ).join(
                RunDao, RunHasDocumentDao.run_id == RunDao.run_id
            ).filter(
                RunDao.corpus_id == corpus_id
            )

            total_count = query.count()

            documents = query.options(subqueryload('*')).limit(page_size).offset(skip).all()

            if not documents:
                logging.debug(f'Documents for corpus with corpus id {corpus_id} have not been found in orbis database.')

            return documents, total_count
        except SQLAlchemyError as e:
            logging.warning(f'Documents for corpus request with corpus id: {corpus_id} failed.')
            logging.debug(f'The following exception occurred: {e}')
            return None, 0

    def count_documents_in_run(self, run_id: int) -> int:
        """
        Count the documents for a given run_id in the database.
        Args:
            run_id: id of the run for which to count the documents.
        Returns: The count as a number.
        """
        count = self.session.query(func.count(DocumentDao.document_id)).join(
            RunHasDocumentDao, DocumentDao.document_id == RunHasDocumentDao.document_id
        ).filter(RunHasDocumentDao.run_id == run_id).scalar()
        return count

    def count_runs_in_gold_standard(self, gold_standard_id: int) -> int:
        """
        Count the runs for a given gold_standard_id in the database
        Args:
            gold_standard_id: id of the gold_standard for which to count the runs
        Returns: the count as a number
        """
        count = self.session.query(func.count(RunDao.run_id)) \
            .filter(RunDao.current_gold_standard_id == gold_standard_id). \
            scalar()
        return count

    def get_documents_of_run(self,
                             run_id: int,
                             page_size: int = None,
                             skip: int = 0
                             ) -> Optional[List[DocumentDao]]:
        """
        Get all documents for a given run from database

        Args:
            run_id: id of the run for which the documents are looked up

        Returns: A list of document objects or None if no document exists for this corpus in the database
        """
        if documents := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).options(subqueryload('*')).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).limit(page_size).offset(skip)).all(),
                f'Documents for run request with run id: {run_id} failed', False
        ):
            return documents
        logging.debug(f'Documents for run with run id {run_id} have not been found in orbis database.')
        return None

    def get_next_document_of_run(self, run_id: int, document_id: int) -> Optional[DocumentDao]:
        """
        Get the next document for the given run.

        Args:
            run_id: id of the run for which the document is looked up.
            document_id: current document id

        Returns: the next document from the run, or None, if no document exists in the database.
        """
        # obtain the next document
        if document := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).where(DocumentDao.document_id > document_id).order_by(DocumentDao.document_id.asc())).first(),
                f'Obtaining the next document for run id: {run_id} and document id: {document_id} failed', False
        ):
            return document

        # no result => return the first document
        if document := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).order_by(DocumentDao.document_id.asc())).first(),
                f'Obtaining the first document for run id: {run_id} failed', False
        ):
            return document

        logging.debug(f'Documents for run with run id {run_id} have not been found in orbis database.')
        return None

    def get_previous_document_of_run(self, run_id: int, document_id: int) -> Optional[DocumentDao]:
        """
        Get the previous document for the given run.
        If called with the id of the first document, the method returns the last one.

        Args:
            run_id: id of the run for which the document is looked up.
            document_id: current document id

        Returns: the previous document from the run, or None, if no document exists in the database.
        """
        # obtain the previous document
        if document := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).where(DocumentDao.document_id < document_id).order_by(DocumentDao.document_id.desc())).first(),
                f'Obtaining the previous document for run id: {run_id} and document id: {document_id} failed', False
        ):
            return document

        # no result => return the last document
        if document := self.try_catch(
                lambda: self.session.scalars(select(DocumentDao).where(
                    DocumentDao.document_id == RunHasDocumentDao.document_id,
                    RunHasDocumentDao.run_id == run_id
                ).order_by(DocumentDao.document_id.desc())).first(),
                f'Obtaining the last document for run id: {run_id} failed', False
        ):
            return document

        logging.debug(f'Documents for run with run id {run_id} have not been found in orbis database.')
        return None

    def get_annotations_of_document_by_run_id(self, run_id: int,
                                              document_id: int) -> Optional[List[DocumentHasAnnotationDao]]:
        """
        Get all annotations for a specific document of a specific run from database

        Args:
            run_id:
            document_id:

        Returns: A list of document annotation objects or None if no according annotation exists in the database
        """
        results = self.try_catch(
            lambda: self.session.scalars(select(DocumentHasAnnotationDao).options(subqueryload('*')).where(
                DocumentHasAnnotationDao.document_id == document_id,
                DocumentHasAnnotationDao.run_id == run_id
            )).all(),
            'Get annotations of document by run id failed',
            [])
        if len(results) > 0:
            return results
        logging.debug(f'There are no annotation entries for run({run_id}) - document({document_id}) combination '
                      f'in orbis database.')
        return None

    def get_annotation_of_document_by_run_id(self, run_id: int,
                                             document_id: int,
                                             annotation_id: int) -> Optional[DocumentHasAnnotationDao]:
        """
        Get specific annotation by id for a specific document of a specific run from database

        Args:
            run_id:
            document_id:
            annotation_id:

        Returns: A single document annotation object or None if no or multiple annotation exists in the database
        """
        if annotation := self.try_catch(
                lambda: self.session.scalars(select(DocumentHasAnnotationDao).options(subqueryload('*')).where(
                    DocumentHasAnnotationDao.annotation_id == annotation_id,
                    DocumentHasAnnotationDao.document_id == document_id,
                    DocumentHasAnnotationDao.run_id == run_id
                )).first(),
                'Get annotation of document by run id failed', None):
            return annotation
        logging.debug(f'There is no annotation entry (id {annotation_id}) for run({run_id}) - document({document_id}) '
                      f'combination in orbis database.')
        return None

    def get_annotations(self) -> Optional[List[AnnotationDao]]:
        """
        Get all annotations from database

        Returns: A list of annotation objects or None if no annotation exists in the database
        """
        try:
            results = self.session.scalars(select(AnnotationDao).options(subqueryload('*'))).all()
            if len(results) > 0:
                return results
            logging.debug('There are no annotation entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All annotations request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')
            return None

    def get_annotation(self, annotation_id: int) -> Optional[AnnotationDao]:
        """
        Get annotation from database.

        Args:
         annotation_id:

        Returns: A single annotation object or None if zero or multiple annotations exists in the database
        """
        return self.try_catch(
            lambda: self.session.scalars(select(AnnotationDao).where(
                AnnotationDao.annotation_id == annotation_id)).first(),
            f'Annotation request with annotation id: {annotation_id} failed', None)

    def get_color_palettes(self) -> List[ColorPalette]:
        """
        Returns: A list of all available ColorPalettes.
        """
        return self.try_catch(
            lambda: self.session.scalars(select(ColorPaletteDao)).all(),
            'Cannot obtain list of available ColorPalettes.', None)

    def get_annotation_type(self, annotation_type_id: int) -> Optional[AnnotationTypeDao]:
        """
        Get annotation type from database.

        Args:
         annotation_type_id:

        Returns: A single annotation type object or None if zero or multiple annotation types exists in the database
        """
        return self.try_catch(
            lambda: self.session.scalars(select(AnnotationTypeDao).where(
                AnnotationTypeDao.type_id == annotation_type_id)).first(),
            f'Annotation type request with annotation type id: {annotation_type_id} failed', None)

    def get_corpus_annotation_types(self, corpus_id: int) -> Dict[AnnotationTypeDao, int]:
        """
        Returns: A list of all supported AnnotationTypes with their corresponding color_ids.
        """
        try:
            results = self.session.scalars(select(CorpusSupportsAnnotationTypeDao).where(
                CorpusSupportsAnnotationTypeDao.corpus_id == corpus_id)).all()
            if len(results) > 0:
                return {csat.annotation_type: csat.color_id for csat in results}
            logging.debug('There are no annotation type entries in orbis database.')
            return {}
        except SQLAlchemyError as e:
            logging.warning('All annotation type request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')

    def set_corpus_annotation_type_color(self, corpus_id: int, annotation_type_id: int, color_id: int) -> None:
        """
        Set the color id of the given annotation type for a corpus.

        Args:
            corpus_id: the corpus for which the annotation type's color is set.
            annotation_type_id: id of the annotation type
            color_id: id of the color (the effective color to used is computed based on `color_id % len(color_palette)`
        """
        csat = CorpusSupportsAnnotationTypeDao(corpus_id=corpus_id, annotation_type_id=annotation_type_id,
                                               color_id=color_id)
        self.session.merge(csat)
        self.commit()

    def get_metadata(self) -> Optional[List[MetadataDao]]:
        """
        Get all metadata from database

        Returns: A list of metadata objects or None if no metadata exists in the database
        """
        try:
            results = self.session.scalars(select(MetadataDao)).all()
            if len(results) > 0:
                return results
            logging.debug('There are no metadata entries in orbis database.')
            return None
        except SQLAlchemyError as e:
            logging.warning('All metadata request failed.')
            logging.debug(f'The following exception occurred: {e.__str__()}')

    def get_metadata_by_id(self, metadata_id: int) -> Optional[MetadataDao]:
        """
        Get metadata from database

        Args:
            metadata_id:

        Returns: A single object of metadata or None if no or multiple metadata exists in the database
        """
        return self.try_catch(
            lambda: self.session.scalars(select(MetadataDao).where(MetadataDao.metadata_id == metadata_id)).first(),
            f'No metadata with id: {metadata_id} found in orbis database.', None)

    def get_annotators(self) -> Optional[List[AnnotatorDao]]:
        """
        Get all annotators from database

        Returns: A list of annotator objects or None if no annotation exists in the database
        """
        try:
            results = self.session.scalars(select(AnnotatorDao).options(subqueryload('*'))).all()
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
        return not (self.session.scalars(
            select(annotation_has_metadata_table).filter_by(metadata_id=metadata_id)).first() or self.session.scalars(
            select(document_has_metadata_table).filter_by(metadata_id=metadata_id)).first())

    def annotation_is_orphan(self, annotation_id: int) -> bool:
        """
        Checks if annotation given by its id is an orphan
        (meaning it's not linked to any document)

        Args:
            annotation_id:

        Returns: True if annotation is an orphan, false otherwise
        """
        return not self.session.scalars(select(DocumentHasAnnotationDao).where(
            DocumentHasAnnotationDao.annotation_id == annotation_id)).first()

    def document_is_orphan(self, document_id: int) -> bool:
        """
        Checks if document given by its id is an orphan
        (meaning it's not linked to any corpus, check is done on run level, since every corpus at least contains one
        default run)

        Args:
            document_id:

        Returns: True if document is an orphan, false otherwise
        """
        return not self.session.scalars(select(RunHasDocumentDao).where(
            RunHasDocumentDao.document_id == document_id)).first()

    def run_is_orphan(self, run_id: int) -> bool:
        """
        Checks if run given by its id is an orphan
        (meaning no documents are linked to it)

        Args:
            run_id:

        Returns: True if run is an orphan, false otherwise
        """
        return not self.session.scalars(select(RunHasDocumentDao).where(
            RunHasDocumentDao.run_id == run_id)).first()

    def annotation_type_is_orphan(self, annotation_type_id: int) -> bool:
        """
        Checks if annotation type given by its id is an orphan
        (meaning it's not linked to any corpora)

        Args:
            annotation_type_id:

        Returns: True if annotation type is an orphan, false otherwise
        """
        return not self.session.scalars(select(CorpusSupportsAnnotationTypeDao).where(
            CorpusSupportsAnnotationTypeDao.annotation_type_id == annotation_type_id)).first()

    def delete_metadata(self, metadata_id: int) -> bool:
        """
        Deletes metadata from orbis database by its id

        Args:
            metadata_id:

        Returns: True if entry could be deleted from orbis database, false otherwise
        """
        if metadata := self.get_metadata_by_id(metadata_id):
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            return (self.try_catch(lambda: not self.session.delete(metadata),
                                   f'Metadata with id {metadata_id} could not be deleted from orbis db.') and
                    self.commit())
        return False

    def delete_orphan_metadata(self, metadata: Set[MetadataDao]) -> bool:
        """
        Checks for each item in a given list of metadata if it's an orphan, if yes, the item will be deleted

        Args:
            metadata:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        # if no metadata is orphan, this statement is true (since: if all([]) -> True)
        if all((self.delete_metadata(m.metadata_id)
                for m in metadata if self.metadata_is_orphan(m.metadata_id))):
            return self.commit()
        return False

    def delete_annotation(self, annotation_id: int) -> bool:
        """
        Delete Annotation from database, relationship to its metadata is also deleted, if a metadata is then an orphan
        it will be deleted.

        Args:
            annotation_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if annotation := self.get_annotation(annotation_id):
            # get the metadata of the annotation before deleting it, otherwise this could cause problems
            metadata = set(annotation.meta_data)
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(annotation),
                               f'Annotation with id {annotation_id} could not be deleted from orbis db.') and
                    self.commit()):
                return self.delete_orphan_metadata(metadata)
        return False

    def delete_orphan_annotations(self, annotations: Set[AnnotationDao]) -> bool:
        """
        Checks for each item in a given list of annotations if it's an orphan, if yes, the item will be deleted

        Args:
            annotations:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all((self.delete_annotation(annotation.annotation_id) for annotation in annotations
                if self.annotation_is_orphan(annotation.annotation_id))):
            return self.commit()
        return False

    def delete_annotation_from_document(self, document_has_annotation: DocumentHasAnnotationDao) -> bool:
        """
        Delete annotation from an existing document in orbis database, further delete the annotation if it's an orphan.

        Args:
            document_has_annotation:

        Returns: True if it worked, false otherwise
        """
        # 'not' isn't necessary in this scenario, session.query().delete() returns number of deleted row, > 0 -> True
        if (self.try_catch(lambda: self.session.query(DocumentHasAnnotationDao).where(
                DocumentHasAnnotationDao.run_id == document_has_annotation.run_id,
                DocumentHasAnnotationDao.document_id == document_has_annotation.document_id,
                DocumentHasAnnotationDao.annotation_id == document_has_annotation.annotation_id).delete(),
                           f'Deleting the annotation_document {document_has_annotation} failed.') and self.commit()):
            if (self.annotation_is_orphan(document_has_annotation.annotation_id) and
                    self.delete_annotation(document_has_annotation.annotation_id)):
                return self.commit()
            return True
        return False

    def delete_document(self, document_id: int) -> bool:
        """
        Delete document from database, relationship to its metadata is also deleted, if a metadata is then an orphan
        it will be deleted.

        Args:
            document_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if document := self.get_document(document_id):
            # get the metadata of the document before deleting it, otherwise this could cause problems
            metadata = set(document.meta_data)
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(document),
                               f'Document with id {document_id} could not be deleted from orbis db.') and
                    self.commit()):
                return self.delete_orphan_metadata(metadata)
        return False

    def delete_orphan_documents(self, documents: Set[DocumentDao]) -> bool:
        """
        Checks for each item in a given list of documents if it's an orphan, if yes, the item will be deleted

        Args:
            documents:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all((self.delete_document(document.document_id) for document in documents
                if self.document_is_orphan(document.document_id))):
            return self.commit()
        return False

    def delete_document_from_corpus(self, document_id: int, corpus_id: int) -> bool:
        """
        Delete document from an existing corpus in orbis database (meaning that the document is deleted from all runs
        of this corpus), further delete the document if it's an orphan.

        Args:
            document_id:
            corpus_id:

        Returns: True if it worked, false otherwise
        """
        # get the runs, documents and annotations before deleting the document, otherwise this could cause problems
        runs = set(self.get_runs_by_corpus_id(corpus_id))
        documents = {self.get_document(document_id)}
        annotations = {document_annotation.annotation
                       for run in runs
                       for run_document in run.run_has_documents if run_document.document_id == document_id
                       for document_annotation in run_document.document_has_annotations}
        if (self.try_catch(lambda: self.session.query(RunHasDocumentDao).where(
                RunHasDocumentDao.run_id == RunDao.run_id,
                RunDao.corpus_id == corpus_id,
                RunHasDocumentDao.document_id == document_id).delete(synchronize_session='fetch'),
                           f'Deleting the document ({document_id}) of corpus ({corpus_id}) failed.') and self.commit()):
            # delete annotation is executed twice (second time in delete run if orphan) but it MUST be executed at this
            # point as well, because an annotation can be orphan even when the run isn't
            return (self.delete_orphan_annotations(annotations) and
                    self.delete_orphan_runs(runs) and
                    self.delete_orphan_documents(documents))
        return False

    def delete_run(self, run_id: int) -> bool:
        """
        Delete run from database, relationship to its documents and to its annotations is also deleted,
        if a document or an annotation is then an orphan it will be deleted.

        Args:
            run_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if run := self.get_run(run_id):
            # get the documents and annotations of the run before deleting it, otherwise this could cause problems
            documents = {run_document.document for run_document in run.run_has_documents}
            annotations = {document_annotation.annotation for run_document in run.run_has_documents
                           for document_annotation in run_document.document_has_annotations}
            # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
            if (self.try_catch(lambda: not self.session.delete(run),
                               f'Run with id {run_id} could not be deleted from orbis db.') and
                    self.commit()):
                return (self.delete_orphan_documents(documents) and
                        self.delete_orphan_annotations(annotations))
        return False

    def delete_orphan_runs(self, runs: Set[RunDao]) -> bool:
        """
        Checks for each item in a given list of runs if it's an orphan, if yes, the item will be deleted

        Args:
            runs:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all((self.delete_run(run.run_id) for run in runs
                if self.run_is_orphan(run.run_id))):
            return self.commit()
        return False

    def delete_annotation_type(self, annotation_type_id: int) -> bool:
        """
        Delete annotation type from database.

        Args:
            annotation_type_id:

        Returns: True if everything worked correctly, false otherwise
        """
        if annotation_type := self.get_annotation_type(annotation_type_id):
            if self.annotation_type_is_orphan(annotation_type_id):
                # 'not' is necessary since session.delete returns None, try_catch expects a boolean, not None -> True
                return (self.try_catch(lambda: not self.session.delete(annotation_type),
                                       f'Annotation type with id {annotation_type_id} '
                                       'could not be deleted from orbis db.') and
                        self.commit())
            logging.warning(f"Annotation type with id {annotation_type_id} could not be deleted, "
                            "it's still associated by corpora.")
        return False

    def delete_orphan_annotation_types(self, annotation_types: Set[AnnotationTypeDao]) -> bool:
        """
        Checks for each item in a given list of annotation types if it's an orphan, if yes, the item will be deleted

        Args:
            annotation_types:

        Returns: True if everything worked correctly (if no orphan is found, True is returned as well), False otherwise
        """
        if all((self.delete_annotation_type(annotation_type.type_id) for annotation_type in annotation_types
                if self.annotation_type_is_orphan(annotation_type.type_id))):
            return self.commit()
        return False

    def delete_corpus(self, corpus_id: int) -> bool:
        """
        Delete corpus from database, relationship to its runs and annotation types is also deleted,
        if a run or an annotation type is then an orphan it will be deleted.

        Args:
            corpus_id:

        Returns: True if everything worked correctly, false otherwise
        """
        have_orphans = False
        if corpus := self.get_corpus(corpus_id):
            supported_annotation_types = {a.annotation_type for a in corpus.supported_annotation_types}
            # first, delete all runs with custom delete_run method,
            # to ensure that all orphan entities are deleted as well
            if not (runs := self.get_runs_by_corpus_id(corpus_id, is_gold_standard=False)):
                runs = []
            if (all((self.delete_run(run.run_id) for run in runs if run)) and
                    # 'not' is necessary since session.delete returns None, try_catch expects a boolean
                    self.try_catch(lambda: not self.session.delete(corpus),
                                   f'Corpus with id {corpus_id} could not be deleted from orbis db.') and
                    self.commit()):
                have_orphans = self.delete_orphan_annotation_types(supported_annotation_types)

            # second, delete the gold standard runs
            if not (gold_standard_runs := self.get_runs_by_corpus_id(corpus_id, is_gold_standard=True)):
                gold_standard_runs = []

            if (all((self.delete_run(run.run_id) for run in gold_standard_runs if run)) and
                    # 'not' is necessary since session.delete returns None, try_catch expects a boolean
                    self.try_catch(lambda: not self.session.delete(corpus),
                                   f'Corpus with id {corpus_id} could not be deleted from orbis db.') and
                    self.commit()):
                have_orphans = have_orphans or self.delete_orphan_annotation_types(supported_annotation_types)

            # delete the list of supported annotation types for that corpus
            for csat in corpus.supported_annotation_types:
                self.session.delete(csat)
            self.commit()
        return have_orphans

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
