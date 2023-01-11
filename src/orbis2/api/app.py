import logging
import sys
import threading
from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI

from orbis2.model.corpus import Corpus
from orbis2.business_logic.orbis_service import OrbisService
from orbis2.config.app_config import AppConfig
from orbis2.metadata import __version__
from pathlib import Path

from orbis2.model.document import Document
from orbis2.model.run import Run

PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'src'))

LOGGING_DIR = PROJECT_DIR / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)

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


@app.get('/getDocuments')
def get_documents(run_id: int = None, corpus_id: int = None) -> List[Document]:
    if run_id:
        return get_orbis_service().get_documents_of_run(run_id)
    if corpus_id:
        return get_orbis_service().get_documents_of_corpus(corpus_id)
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


@app.post('/addCorpus/')
def add_corpus(corpus: Corpus) -> Corpus:
    return corpus


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63019)
