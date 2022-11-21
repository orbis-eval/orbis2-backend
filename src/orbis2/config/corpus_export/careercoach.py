import json
from itertools import chain
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

from orbis2.corpus_import.format import CorpusFormat
from orbis2.corpus_import.format.careercoach import SEGMENT_TYPE_PREFIX
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.document import Document
from orbis2.model.role import Role
from orbis2.model.run import Run


def get_export_doc_name(document: Document) -> str:
    normalized_url = urlparse(document.key).netloc
    return '{normalized_url}_i{document.document_id}.json'


def get_entity_annotations(annotations):
    pass


def get_segment_annotations(annotations):
    return [{} for annotation in annotations
            if annotation.annotation_type.name.startswith(SEGMENT_TYPE_PREFIX)]


class CareerCoachFormat:
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """
    @staticmethod
    def export(run: Run, path: Path):
        for document, annotations in run.document_annotations.items():
            with path.joinpath(get_export_doc_name(document)).open('w') as f:
                export_doc = {
                    'id': document.document_id,
                    'url': document.key,
                    'text': document.content,
                    'gold_standard_annotation': get_entity_annotations(annotations),
                    'gold_standard_annotation_segmentation': get_segment_annotations(annotations)
                }
                json.dump(export_doc, f)
