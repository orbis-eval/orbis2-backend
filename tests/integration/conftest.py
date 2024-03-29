import os
import pytest as pytest
from xxhash import xxh32_hexdigest

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role
from orbis2.model.run import Run


@pytest.fixture(scope='session', autouse=True)
def create_database():
    os.environ['ORBIS_DB_NAME'] = 'orbis_test'

    assert OrbisDb().create_database(True)


@pytest.fixture()
def clear_test_data_orbis():
    assert OrbisDb().clear_tables()


@pytest.fixture()
def insert_test_data_orbis(clear_test_data_orbis):
    run = Run(
        'run1', 'run1', Corpus('corpus1', [AnnotationType('annotation-type1', color_id=1)]),
        {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
         [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1', color_id=1),
                     Annotator('Andreas', [Role('admin')], xxh32_hexdigest('test1234')),
                     metadata=[Metadata('key2', 'value2')])]})
    assert OrbisService().add_run(run)


@pytest.fixture()
def insert_test_data_multiple_documents(clear_test_data_orbis):
    test_annotation = Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1', color_id=1),
                                 Annotator('Andreas', [Role('admin')], xxh32_hexdigest('test1234')),
                                 metadata=[Metadata('key2', 'value2')])
    run = Run(
        'run2', 'run2', Corpus('corpus1', [AnnotationType('annotation-type1', color_id=1)]),
        {Document('Text, this is document one.', metadata=[Metadata('key1', 'value1')]): [test_annotation],
         Document('Text, this is document two.', metadata=[Metadata('key1', 'value1')]): [test_annotation],
         Document('Text, this is document three.', metadata=[Metadata('key1', 'value1')]): [test_annotation],
         Document('Text, this is document four.', metadata=[Metadata('key1', 'value1')]): [test_annotation],
         Document('Text, this is document five.', metadata=[Metadata('key1', 'value1')]): [test_annotation],
         })
    assert OrbisService().add_run(run)
