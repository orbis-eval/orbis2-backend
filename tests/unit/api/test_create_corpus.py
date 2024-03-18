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
        'file': {}
    })

    assert response.status_code == 201
def test_create_corpus_with_valid_jsonl_file():
    client = TestClient(app)
    file_content = """{"id":1,"text":"Mitarbeitende und Studierende der FH Graubünden erhalten einen Rabatt von CHF 4.- auf die Menüs im Coop Restaurant Chur West. Die Mindestkonsumation beträgt dabei CHF 9.95 – das günstigste Menü. Der Rabatt gilt nur für Menüs und ist zeitlich von 11 bis 14 Uhr beschränkt. Das Angebot gilt von Montag bis und mit Samstag. Um vom Rabatt profitieren zu können, muss vor der Bezahlung ein Mitarbeitenden- oder Studierendenausweis vorgelegt werden. Der Rabatt kann nicht auf andere Personen übertragen werden.","label":[[0,13,"PER"],[18,29,"PER"],[34,47,"ORG"],[99,125,"ORG"],[130,148,"MISC"],[189,193,"OBJ"],[276,283,"OBJ"],[328,334,"MISC"],[406,425,"OBJ"],[477,485,"PER"]],"Comments":[]}
{"id":2,"text":"Die Mensa der Fachhochschule Graubünden freut sich darauf, Sie täglich mit ihren köstlichen Kreationen zu begeistern. Ob täglich wechselnder Speiseplan oder selbst zubereitete Köstlichkeiten vom Markt und Salatbuffet, Sie werden bestimmt etwas finden, das Ihnen schmeckt. Kaffee und Desserts werden natürlich auch angeboten. Probieren Sie das reichhaltige Angebot an Speisen!","label":[[4,9,"MISC"],[14,39,"ORG"],[205,216,"OBJ"],[272,278,"OBJ"],[283,291,"OBJ"],[335,338,"PER"]],"Comments":[]}
"""

    response = client.post('/createCorpus', json={
        'corpus': {
            'name': 'test_corpus',
            'supported_annotation_types': []
        },
        'file': {
            'filename': 'test.jsonl',
            'file_format': '.jsonl',
            'content': file_content
        }
    })

    assert response.status_code == 201
def test_create_corpus_with_invalid_jsonl_file():
    client = TestClient(app)

    response = client.post('/createCorpus', json={
        'corpus': {
            'name': 'test_corpus',
            'supported_annotation_types': []
        },
        'file': {
            'filename': 'test.jsonl',
            'file_format': '.jsonl',
            'content': 'test content'
        }
    })

    assert response.status_code == 400