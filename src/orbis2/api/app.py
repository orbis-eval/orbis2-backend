import sys
import threading
from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI, Response, status

from orbis2.model.annotation import Annotation
from orbis2.model.corpus import Corpus
from orbis2.business_logic.orbis_service import OrbisService
from orbis2.metadata import __version__
from pathlib import Path

from orbis2.model.document import Document
from orbis2.model.run import Run

PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'src'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'orbis2'))

LOGGING_DIR = PROJECT_DIR / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
# logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)

ORBIS_SERVICE_LAZY_INIT_LOCK = threading.Lock()
DOCUMENTS_LAZY_INIT_LOCK = threading.Lock()

app = FastAPI(
    title='Orbis2 Backend',
    version=__version__
)

global_orbis_service = None


def get_orbis_service() -> OrbisService:
    global global_orbis_service
    with ORBIS_SERVICE_LAZY_INIT_LOCK:
        if not global_orbis_service:
            global_orbis_service = OrbisService()
        return global_orbis_service


@app.get('/getAnnotations')
def get_annotations(run_id: int = None, document_id: int = None) -> List[Annotation]:
    return get_orbis_service().get_annotations(run_id, document_id)


@app.get('/getDocuments')
def get_documents(run_id: int = None, corpus_id: int = None, page_size: int = None, skip: int = 0) -> List[Document]:
    if run_id:
        # TODO, anf 08.02.2023: implement pagination also for get docs of run
        return get_orbis_service().get_documents_of_run(run_id)
    if corpus_id:
        return get_orbis_service().get_documents_of_corpus(corpus_id, page_size, skip)
    return get_orbis_service().get_documents()


@app.get('/getDocument')
def get_document(document_id: int) -> Document:
    # TODO, anf 13.12.2022: implement response in error case
    if document_id:
        return get_orbis_service().get_document(document_id)


@app.get('/getRuns')
def get_runs(corpus_id: int = None) -> List[Run]:
    if corpus_id:
        return get_orbis_service().get_run_names(corpus_id)
    return get_orbis_service().get_run_names()


@app.get('/getCorpora')
def get_corpora() -> List[Corpus]:
    return get_orbis_service().get_corpora()


@app.get('/getCorpus')
def get_corpus(corpus_id: int) -> Corpus:
    return get_orbis_service().get_corpus(corpus_id)


@app.post('/addCorpus')
def add_corpus(corpus: Corpus, documents: List[Document] = []) -> Corpus:
    print(corpus)
    print(documents)
    run = Run(f'default_{corpus.name}', f'default run for corpus {corpus.name}, no annotations',
              corpus, {document: [] for document in documents})
    get_orbis_service().add_run(run)
    return corpus


@app.post('/addAnnotation')
def add_annotation(annotation: Annotation) -> Annotation:
    return get_orbis_service().add_annotation_to_document(annotation)


@app.delete('/removeAnnotationFromDocument', status_code=200)
def remove_annotation_from_document(annotation: Annotation, response: Response):
    if get_orbis_service().remove_annotation_from_document(annotation):
        return
    response.status_code = status.HTTP_400_BAD_REQUEST
    return


@app.delete('/removeCorpus', status_code=200)
def remove_corpus(corpus: Corpus, response: Response):
    if get_orbis_service().remove_corpus(corpus._id):
        return
    response.status_code = status.HTTP_400_BAD_REQUEST
    return


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63012)
