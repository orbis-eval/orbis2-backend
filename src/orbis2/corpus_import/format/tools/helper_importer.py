from typing import List
from .labelstudio_importer import LabelStudioImporter
from .doccano_importer import DoccanoImporter


class HelperImporter:
    @staticmethod
    def get_annotated_documents_and_types(file: dict = None) -> tuple:
        documents_with_annotations_list = []
        annotation_types = []

        if file:
            if file["filename"].endswith(".json"):
                documents_with_annotations_list.extend(LabelStudioImporter.get_annotated_documents(file))
                annotation_types = list(set(annotation_types + LabelStudioImporter.get_annotation_types(file)))
            elif file["filename"].endswith(".jsonl"):
                documents_with_annotations_list.extend(DoccanoImporter.get_annotated_documents(file))
                annotation_types = list(set(annotation_types + DoccanoImporter.get_annotation_types(file)))
            else:
                raise ValueError(f"Unknown file format {file['file_format']}.")

        return documents_with_annotations_list, annotation_types
