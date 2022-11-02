from builtins import staticmethod
from typing import List, Dict


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
    def get_document_content(document_list: List[str]) -> List[str]:
        """
        Extract the corpus documents.

        :param document_list: A list of the corpus documents and annotations.
        :return: A list that contains the document content.
        """
        raise NotImplementedError

    @staticmethod
    def get_document_annotations(document_list: List[str]) -> Dict:
        """
        Extract the corpus annotations.

        :param document_list: A list of the corpus documents and annotations.
        :return: A dictionary that maps document_ids to the corresponding list
         of annotations
        """
        raise NotImplementedError