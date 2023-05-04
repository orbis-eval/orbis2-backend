from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.metadata import Metadata
from json import dumps, loads


def test_metadata_initialization():
    """
    Verify that the metadata object is correctly initialized by pydantic.
    """
    metadata = Metadata('key1', 'value1')
    assert metadata.key == 'key1'
    assert metadata.value == 'value1'
    assert metadata._id != 0

def test_metadata_json_serialization():
    metadata = Metadata('key1', 'value1')
    assert metadata.json()


def test_metadata_list_json_serialization_and_deserialization():
    """
    Verify that Metadata objects in a list get correctly serialized _and_ deserialized.
    """
    class MetadataList(OrbisPydanticBaseModel):
        name: str
        metadata: list[Metadata]

        def __hash__(self):
            return hash((self.name, tuple(self.metadata)))

        def __eq__(self, other):
            if not isinstance(other, MetadataList):
                return False
            return self.name == other.name and self.metadata == other.metadata


    meta_list = MetadataList(name="test", metadata= [
        Metadata('partition', 'requirements'),
        Metadata('type', 'table')
    ])

    json = dumps(OrbisPydanticBaseModel.remove_id_fields(meta_list.dict()))
    print(json)

    meta_list2 = MetadataList.parse_raw(json)
    assert meta_list2 == meta_list



