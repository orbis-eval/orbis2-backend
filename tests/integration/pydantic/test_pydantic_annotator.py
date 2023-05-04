from xxhash import xxh32_hexdigest

from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role


def test_annotator_initialization():
    annotator = Annotator('Andreas', [Role('admin')])
    assert annotator.name == 'Andreas'
    assert annotator.roles == [Role('admin')]
    assert annotator.password == xxh32_hexdigest('')


def test_annotator_json_serialization():
    annotator = Annotator('Andreas', [Role('admin')])
    assert annotator.json()