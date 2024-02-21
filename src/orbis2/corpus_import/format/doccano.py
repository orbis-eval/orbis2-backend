from orbis2.model.document import Document
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.role import Role
from orbis2.model.metadata import Metadata


import json
from typing import List

class DoccanoImporter:
    def __init__(self):
        pass
    @staticmethod
    def get_annotated_documents(file: dict) -> List[Document]:
        content = []
        for line in file["content"].splitlines():
            document_raw = json.loads(line)
            content.append(document_raw)
        documents = []
        for document_raw in content:
            annotations = []
            if "label" in document_raw:
                for annotation in document_raw["label"]:
                    start = annotation[0]
                    end = annotation[1]
                    annotations_type = annotation[2]
                    annotations.append(
                        Annotation(
                            'text',
                            document_raw["text"].strip()[start:end],
                            start,
                            end,
                            AnnotationType(annotations_type),
                            Annotator("none", [Role('admin')]),
                            metadata=[]
                        )
                    )
            document = Document(
                content=document_raw["text"].strip(),
                metadata=[],
            )
            documents.append([document, annotations])
        return documents

    @staticmethod
    def get_annotation_types(file: dict) -> List[str]:
        content = []
        for line in file["content"].splitlines():
            document_raw = json.loads(line)
            content.append(document_raw)
        annotation_types = []
        for document_raw in content:
            if "label" in document_raw:
                for annotation in document_raw["label"]:
                    annotation_types.append(annotation[2])
        annotation_types = list(set(annotation_types))
        return annotation_types
