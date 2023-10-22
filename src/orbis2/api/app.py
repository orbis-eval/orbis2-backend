import sys
import threading
from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

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

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        return get_orbis_service().get_documents_of_run(run_id, page_size, skip)
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


@app.post('/createCorpus')
def create_corpus(corpus: Corpus, documents: List[Document] = None) -> Corpus:
    if not documents:
        documents = []
    run = Run(f'default_{corpus.name}', f'default run for corpus {corpus.name}, no annotations',
              corpus, {document: [] for document in documents})
    get_orbis_service().add_run(run)
    return corpus


@app.post('/createRun')
def create_run(corpus: Corpus, run_name: str, run_description: str) -> dict[str, list[Document]]:
    if corpus and run_name and run_description:
        run = Run(run_name, run_description, corpus,
                  {document: [] for document in get_orbis_service().get_documents_of_corpus(corpus._id)})
        if get_orbis_service().add_run(run):
            # return the id and the documents from the run
            run.document_annotations = None
            return {'id': run._id, 'documents': get_orbis_service().get_documents_of_run(run._id)}


@app.delete('/deleteRun', status_code=200)
def delete_run(run: Run, response: Response) -> {}:
    if get_orbis_service().delete_run(run._id):
        message = f"Run with ID {run._id} has been deleted successfully."
        return JSONResponse(content={"message": message})
    else:
        message = f"Failed to delete Run with ID {run._id}."
        response.status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={"message": message})

@app.post('/createAnnotation')
def create_annotation(annotation: Annotation) -> Annotation:
    return get_orbis_service().add_annotation_to_document(annotation)


@app.delete('/deleteAnnotationFromDocument', status_code=200)
def delete_annotation_from_document(annotation: Annotation, response: Response):
    if get_orbis_service().delete_annotation_from_document(annotation):
        return
    response.status_code = status.HTTP_400_BAD_REQUEST


@app.delete('/deleteCorpus', status_code=200)
def delete_corpus(corpus: Corpus, response: Response):
    if get_orbis_service().delete_corpus(corpus._id):
        return
    response.status_code = status.HTTP_400_BAD_REQUEST


@app.get('/nextDocument', status_code=200)
def next_document(run_id: int, document_id: int):
    return get_orbis_service().get_next_document(run_id, document_id)


@app.get('/previousDocument', status_code=200)
def previous_document(run_id: int, document_id: int):
    return get_orbis_service().get_previous_document(run_id, document_id)


@app.get('/countDocuments', status_code=200)
def count_documents(run_id: int):
    return get_orbis_service().count_documents_in_run(run_id)


@app.get('/colorPalettes', status_code=200)
def color_palettes():
    return get_orbis_service().get_color_palettes()


@app.get('/corpusAnnotationTypes', status_code=200)
def get_corpus_annotation_types(corpus_id: int):
    return get_orbis_service().get_corpus_annotation_types(corpus_id)


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63012)
