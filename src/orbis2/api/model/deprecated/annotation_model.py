from typing import Dict, List

from pydantic import BaseModel, Field


class AnnotationModel(BaseModel):
    key: str = Field(..., description='Key which uniquely assigns the element to the corresponding entry '
                                      'in the x28 ontology.')
    type: str = Field(..., description='Annotation type.')
    surface_form: str = Field(..., description='Annotated element as it is written '
                                               'in the text representation of the html.')
    start: int = Field(..., description='Start position of the annotated element '
                                        'in the text representation of the html.')
    end: int = Field(..., description='Start position of the annotated element in the text representation of the html.')
    scope: str = Field(..., description='Scope of the annotations')
    meta: Dict

    class Config:
        schema_extra = {
            "example":
                {
                    "key": "#somekey",
                    "type": "topic",
                    "surface_form": "Hello world",
                    "start": 21,
                    "end": 32,
                    "scope": "some_scope",
                    "meta": {"some": "other",
                             "key": "values"}
                }
        }