import json
from jsonschema import validate
from typing import List

from orbis2.model.document import Document
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.role import Role
from .base_importer import BaseImporter

LABEL_STUDIO_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "annotations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "result": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "object",
                                        "properties": {
                                            "start": {
                                                "type": "integer"
                                            },
                                            "end": {
                                                "type": "integer"
                                            },
                                            "text": {
                                                "type": "string"
                                            },
                                            "labels": {
                                                "type": "array",
                                                "items": {
                                                    "type": "string"
                                                }
                                            }
                                        },
                                        "required": ["start", "end", "text", "labels"]
                                    },
                                    "from_name": {
                                        "type": "string"
                                    },
                                    "to_name": {
                                        "type": "string"
                                    },
                                    "type": {
                                        "type": "string"
                                    },
                                    "origin": {
                                        "type": "string"
                                    }
                                },
                                "required": ["value", "from_name", "to_name", "type", "origin"]
                            }
                        }
                    },
                    "required": ["id", "result"]
                }
            },
            "data": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string"
                    }
                },
                "required": ["text"]
            },
            "updated_by": {
                "type": "integer"
            }
        },
        "required": ["id", "annotations", "data", "updated_by"]
    }
}


class LabelStudioImporter(BaseImporter):
    @staticmethod
    def validate(file: dict) -> bool:
        content = json.loads(file["content"])
        return validate(content, LABEL_STUDIO_SCHEMA)

    @staticmethod
    def get_annotated_documents(file: dict) -> List[Document]:
        LabelStudioImporter.validate(file)
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
