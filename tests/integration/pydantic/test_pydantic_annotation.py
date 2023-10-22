from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role
from json import dumps


def test_annotation_initialization():
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    assert annotation.surface_forms == ('Text',)
    assert annotation.start_indices == (0,)
    assert annotation.end_indices == (4,)
    assert annotation.annotation_type == AnnotationType('annotation-type1')
    assert annotation.annotator == Annotator('Andreas', [Role('admin')])
    assert annotation.metadata == [Metadata('key1', 'value1'), Metadata('key2', 'value2')]


def test_annotation_json_serialization_and_deserialization():
    """
    Ensure that the given annotation object is correctly serialized and deserialized.
    """
    annotation = Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                            metadata=[Metadata('key1', 'value1'), Metadata('key2', 'value2')])
    annotation_json = dumps(OrbisPydanticBaseModel.delete_id_fields(annotation.dict()))

    deserialized_annotation = Annotation.parse_raw(annotation_json)
    assert deserialized_annotation == annotation
    assert deserialized_annotation.metadata == annotation.metadata
    assert deserialized_annotation.annotator == annotation.annotator


def test_parsing_annotation_with_fixed_metadata():
    annotation_json_data = """
    {
        "key": "url",
        "surface_forms": [
            "Beispiel"
        ],
        "start_indices": [
            18
        ],
        "end_indices": [
            26
        ],
        "annotation_type": {
            "name": "annotation-type2"
        },
        "annotator": {
            "name": "Norman",
            "roles": [
                {
                    "name": "annotator"
                }
            ],
            "password": "02cc5d05"
        },
        "run_id": 3426845003,
        "document_id": 615516308,
        "metadata": [
            {
                "key": "key2",
                "value": "value2"
            }
        ],
        "timestamp": "2023-05-03T16:12:05.362737"
    }
    """
    parsed_annotation = Annotation.parse_raw(annotation_json_data)
    print(parsed_annotation.json())
