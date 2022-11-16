from builtins import staticmethod
from itertools import chain
from typing import List, Dict

from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.document import Document


class CorpusFormat:

    @staticmethod
    def is_supported(document_list: List[str]):
        """
        Determine whether the given document list is supported by the
        CorpusFormat.

        :param document_list: A list of documents and annotations.
        :return: True, if the given CorpusFormat supports the provided format.
        """
        raise NotImplementedError

    @staticmethod
    def get_document_content(document_list: List[str]) -> List[Document]:
        """
        Extract the corpus documents.

        :param document_list: A list of the corpus documents and annotations.
        :return: A list that contains the document content.
        """
        raise NotImplementedError

    @staticmethod
    def get_document_annotations(document_list: List[str]) -> Dict[Document, List[Annotation]]:
        """
        Extract the corpus annotations.

        :param document_list: A list of the corpus documents and annotations.
        :return: A dictionary that maps document_ids to the corresponding list
         of annotations
        """
        raise NotImplementedError

    @staticmethod
    def get_supported_annotation_types(document_annotations: Dict[Document, List[Annotation]]) -> List[AnnotationType]:
        """
        Return:
            The annotation types that are supported by the corpus.
        """
        return list({annotation.annotation_type for annotation in chain(*document_annotations.values())})
