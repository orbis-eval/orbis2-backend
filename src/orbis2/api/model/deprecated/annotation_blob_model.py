from typing import Dict, List

from pydantic import BaseModel, Field

from orbis2.api.model.deprecated.annotation_model import AnnotationModel


class AnnotationBlobModel(BaseModel):
    d_id: str = Field(..., description='Unique key for identifying document')
    meta: Dict
    annotations: List[AnnotationModel]

    class Config:
        schema_extra = {
            "example":
                {"d_id": "some_document_id",
                 "meta": {"some": "annotator",
                          "and": "iteration",
                          "or": "creation_date"},
                 "annotations": [{
                     "key": "#somekey",
                     "type": "topic",
                     "surface_form": "Hello world",
                     "start": 21,
                     "end": 32,
                     "scope": "some_scope",
                     "meta": {"some": "other",
                              "key": "values"}
                 }]}
        }
