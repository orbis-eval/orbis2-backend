from orbis2.model.document import Document
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.role import Role
from orbis2.model.metadata import Metadata


import json
from typing import List

class LabelStudioImporter:
    def __init__(self):
        pass
    @staticmethod
    def get_annotated_documents(file: dict) -> List[Document]:
        content = json.loads(file["content"])
        documents = []
        for document_raw in content:
            annotations = []
            if "annotations" in document_raw:
                for annotation in document_raw["annotations"]:
                    if "result" in annotation:
                        for result in annotation["result"]:
                            if "value" in result:
                                for annotations_type in result["value"]["labels"]:
                                    annotations.append(
                                        Annotation(
                                            'text',
                                            result["value"]["text"],
                                            result["value"]["start"] - 1,
                                            result["value"]["end"],
                                            AnnotationType(annotations_type),
                                            Annotator(str(document_raw['updated_by']), [Role('admin')]),
                                            metadata=[]
                                        )
                                    )
            document = Document(
                content=document_raw["data"]["text"].strip(),
                metadata=[],
            )
            documents.append([document, annotations])
        return documents

    @staticmethod
    def get_annotation_types(file: dict) -> List[str]:
        content = json.loads(file["content"])
        annotation_types = []
        for document_raw in content:
            if "annotations" in document_raw:
                for annotation in document_raw["annotations"]:
                    if "result" in annotation:
                        for result in annotation["result"]:
                            if "value" in result:
                                annotation_types = list(set(annotation_types + result["value"]["labels"]))
        return annotation_types
