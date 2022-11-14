import json
from itertools import chain
from typing import List, Dict

from orbis2.corpus_import.format import CorpusFormat

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.database.orbis.entities.annotation_type_dao import \
    AnnotationTypeDao
from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.database.orbis.entities.document_dao import DocumentDao
from orbis2.database.orbis.entities.document_has_annotation_dao import \
    DocumentHasAnnotationDao
from orbis2.database.orbis.entities.role_dao import RoleDao
from orbis2.database.orbis.entities.run_has_document_dao import \
    RunHasDocumentDao

IMPORT_ANNOTATOR_ROLE = RoleDao(name='CareerCoachFormat Importer')
ANNOTATOR = AnnotatorDao(name='AnnotatorName', roles=[IMPORT_ANNOTATOR_ROLE])


class CareerCoachFormat(CorpusFormat):
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    @staticmethod
    def is_supported(document_list: List[str]):
        try:
            doc = json.loads(document_list[0])
        except json.decoder.JSONDecodeError:
            return False

        for key in 'text', 'gold_standard_annotation':
            if key not in doc:
                return False

        try:
            annotation = list(
                doc['gold_standard_annotation'].values()).pop().pop()
            assert 'surface_form' in annotation
            assert 'start' in annotation
            assert 'end' in annotation
            return True
        except:
            return False

    @staticmethod
    def get_run_documents(document_list: List[str]) -> List[RunHasDocumentDao]:
        """
        TODO: add document['url'] to dao and loop
        """
        return [RunHasDocumentDao(
            document=DocumentDao(content=doc['text']),
            document_has_annotations=[DocumentHasAnnotationDao(
                annotation=AnnotationDao(
                    key=annotation['key'],
                    annotation_type=AnnotationTypeDao(name=annotation['type']),
                    annotator=ANNOTATOR,
                    surface_forms=[annotation['surface_form']],
                    start_indices=[annotation['start']],
                    end_indices=[annotation['end']]
                ))
                for annotation in
                chain(*doc['gold_standard_annotation'].values())],
            done=True)  # to be determined
            for doc in map(json.loads, document_list)]

    @staticmethod
    def get_document_content(document_list: List[str]) -> List[str]:
        return [doc['text'] for doc in map(json.loads, document_list)]

    @staticmethod
    def get_document_annotations(document_list: List[str]) -> Dict:
        return {hash(doc['text']): list(chain(
            *doc['gold_standard_annotation'].values()))
            for doc in map(json.loads, document_list)
        }
