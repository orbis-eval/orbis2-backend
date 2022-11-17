from pydantic import BaseModel, Field

from orbis2.api.model.deprecated.annotation_blob_model import AnnotationBlobModel


class DataExchangeModel(BaseModel):
    da_id: str = Field(..., description='Unique key for identifying document annotations')
    annotator: str = Field(..., description='Name of the annotator')
    data: AnnotationBlobModel

    class Config:
        schema_extra = {
            "example":
                {
                    "da_id": "some_da_id",
                    "annotator": "some_annotator",
                    "data": {"d_id": "some_document_id",
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
        }
