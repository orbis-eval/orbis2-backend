import json
from itertools import groupby
from typing import List, Dict, Union

from orbis2.corpus_import.format import CorpusFormat
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role

SEGMENT_TYPE_PREFIX = 'segment/'

ANNOTATOR = Annotator(name='CorpusImporter', roles=[Role(name='CorpusImporter')])


def get_type_or_proposed_type(annotation: Union[Annotation, Dict]) -> str:
    """
    Return:
        The type for the given key.
    """
    if 'type' not in annotation:
        return 'page-segment'

    return annotation['key'].split('#')[1].split("/")[0] if annotation['type'] == 'proposal' else \
        annotation['type']


class CareerCoachFormat(CorpusFormat):
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    @staticmethod
    def is_supported(document_list: List[str], partition: str):
        try:
            doc = json.loads(document_list[0])
        except json.decoder.JSONDecodeError:
            return False
        return all(not key not in doc for key in ('text', partition))

    @staticmethod
    def get_document_annotations(document_list: List[str], invalid_annotation_types: List[str],
                                 partition: str = 'gold_standard_annotation', ) -> Dict[Document, List[Annotation]]:
        """
        Return:
            A dictionary of documents and corresponding annotations for import.
        """

        def segment_generator(partition_annotation_list):
            for segment_name, annotations in partition_annotation_list.items():
                for annotation in annotations:
                    yield segment_name, annotation

        document_annotations = {}
        for doc in map(json.loads, document_list):
            annotations = []
            document_annotations[Document(content=doc['text'], key=doc['url'])] = annotations
            for segment_name, annotation in segment_generator(doc[partition]):
                annotation_type = annotation.get("type",
                                                 annotation.get('entity_type', f'{SEGMENT_TYPE_PREFIX}/{segment_name}'))

                if annotation_type not in invalid_annotation_types:
                    annotations.append(
                        Annotation(key=annotation['key'] if 'key' in annotation and
                                                            annotation_type != 'proposal' else None,
                                   surface_forms=annotation['phrase'] if 'phrase' in annotation else annotation[
                                       'surface_form'],
                                   start_indices=annotation['start'],
                                   end_indices=annotation['end'],
                                   annotation_type=AnnotationType(get_type_or_proposed_type(annotation)),
                                   metadata=[Metadata(key="segment", value=segment_name)],
                                   annotator=ANNOTATOR)
                    )
        return document_annotations

    @staticmethod
    def delete_overlapping_proposals(annotation_list: List[Annotation]) -> List[Annotation]:
        """
        Delete proposals that overlap an annotation of the same type.
        (e.g. proposal-education and education)
        """
        annotations = []
        for _, identical_annotations in groupby(sorted(annotation_list), lambda a: (
                tuple(a.start_indices), tuple(a.end_indices))):
            ia = list(identical_annotations)
            for annotation in ia:
                if len(list(ia)) != 1:
                    print(len(ia), ia)
                if annotation.annotation_type != 'proposal':
                    annotations.append(annotation)
                else:
                    proposal_type = annotation.key.split("#")[1]
                    if proposal_type not in [a.get('type', '') for a in ia]:
                        annotations.append(annotation)
        return annotations

    @staticmethod
    def get_document_content(document_list: List[str]) -> List[Document]:
        pass
