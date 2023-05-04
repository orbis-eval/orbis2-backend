from orbis2.model.metadata import Metadata


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