from orbis2.api.app import app
from orbis2.model.corpus import Corpus
from fastapi.testclient import TestClient

def test_create_corpus():
    client = TestClient(app)

    response = client.post('/createCorpus', json={
        'corpus': {
            'name': 'test_corpus',
            'supported_annotation_types': []
        },
        'files': []
    })

    assert response.status_code == 201