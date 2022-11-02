import json

from itertools import chain
from typing import List, Dict
from orbis2.corpus_import.format import CorpusFormat


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
    def get_document_content(document_list: List[str]) -> List[str]:
        return [doc['text'] for doc in map(json.loads, document_list)]

    @staticmethod
    def get_document_annotations(document_list: List[str]) -> Dict:
        return {hash(doc['text']): list(chain(
            *doc['gold_standard_annotation'].values()))
            for doc in map(json.loads, document_list)
        }