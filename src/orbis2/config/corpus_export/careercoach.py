import json
from itertools import groupby
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

from orbis2.corpus_import.format.careercoach import SEGMENT_TYPE_PREFIX
from orbis2.model.annotation import Annotation
from orbis2.model.document import Document
from orbis2.model.run import Run

PROPOSAL_PREFIX = 'https://semanticlab.net/career-coach#{}/'


def get_export_doc_name(document: Document) -> str:
    normalized_url = urlparse(document.key).netloc
    return f'{normalized_url}_i{hash(document)}.json'


def get_entity_annotations(annotations: List[Annotation]) -> Dict[str, List[Dict[str, str]]]:
    def get_page_segment(annotation: Annotation) -> str:
        return None if not annotation.metadata else \
            max((metadata.value for metadata in annotation.metadata if metadata.key == 'segment'))

    def get_entity_annotation_dict(annotation: Annotation) -> Dict[str, str]:
        return {
            'surface_form': annotation.surface_forms[0],
            'start': annotation.start_indices[0],
            'end': annotation.end_indices[0],
            'key': annotation.key if annotation.key else PROPOSAL_PREFIX.format(annotation.annotation_type.name),
            'type': annotation.annotation_type.name if annotation.key else "proposal"
        }

    return {
        page_segment: list(map(get_entity_annotation_dict, partition_annotations))
        for page_segment, partition_annotations in groupby(sorted(annotations, key=get_page_segment),
                                                           get_page_segment)
        if page_segment
    }


def get_segment_annotations(annotations):
    def get_page_segment(annotation: Annotation) -> str:
        return "" if not annotation.annotation_type.name.startswith(SEGMENT_TYPE_PREFIX) else \
            annotation.annotation_type.name.split(SEGMENT_TYPE_PREFIX)[1]

    def get_segment_annotation_dict(annotation: Annotation) -> Dict[str, str]:
        return {
            'surface_form': annotation.surface_forms[0],
            'start': annotation.start_indices[0],
            'end': annotation.end_indices[0],
            'content_type': 'Text'
        }

    return [{page_segment: list(map(get_segment_annotation_dict, segment_annotations))}
            for page_segment, segment_annotations in groupby(sorted(annotations, key=get_page_segment),
                                                             get_page_segment)
            if page_segment]


class CareerCoachExportFormat:
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    @staticmethod
    def export(run: Run, path: Path):
        for document, annotations in run.document_annotations.items():
            with path.joinpath(get_export_doc_name(document)).open('w') as f:
                export_doc = {
                    'id': hash(document),
                    'url': document.key,
                    'text': document.content,
                    'gold_standard_annotation': get_entity_annotations(annotations),
                    'gold_standard_annotation_segmentation': get_segment_annotations(annotations)
                }
                json.dump(export_doc, f, indent=True)
