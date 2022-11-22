import logging.config
import sys
import threading
from typing import Union, Tuple

import uvicorn as uvicorn
from fastapi import FastAPI

from orbis2.api.model.deprecated.data_exchange_model import DataExchangeModel
from orbis2.api.model.deprecated.response import Response
from orbis2.api.model.deprecated.response_model import ResponseModel
from orbis2.business_logic.orbis_service import OrbisService
from orbis2.config.app_config import AppConfig
from orbis2.metadata import __version__
from pathlib import Path

from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.run import Run


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

LOGGING_DIR = PROJECT_DIR / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

ORBIS_SERVICE_LAZY_INIT_LOCK = threading.Lock()
DOCUMENTS_LAZY_INIT_LOCK = threading.Lock()

app = FastAPI(
    title='Orbis2 Backend',
    version=__version__
)

global_orbis_service = None
global_document_ids = None
global_document_id_index = 2


def get_orbis_service() -> OrbisService:
    global global_orbis_service
    with ORBIS_SERVICE_LAZY_INIT_LOCK:
        if not global_orbis_service:
            global_orbis_service = OrbisService()
        return global_orbis_service


def get_document_id(index: int) -> str:
    """
    Get a generator over all documents, each given by 'run_id|document_id'

    Args:
        index: relative index from the current position

    Returns: run-document id
    """
    global global_document_ids
    global global_document_id_index
    with DOCUMENTS_LAZY_INIT_LOCK:
        if not global_document_ids:
            global_document_ids = []
            if ((corpus_id := get_orbis_service().get_corpus_id('careercoach2022')) and
               (runs := get_orbis_service().get_runs_by_corpus_id(corpus_id))):
                run = runs[0]
                documents = list(run.document_annotations.keys())
                global_document_ids = sorted([run.run_id.__str__() + '|' + document.document_id.__str__()
                                              for document in documents])

        global_document_id_index = (global_document_id_index + int(index)) % len(global_document_ids)
        logging.info(f'Current index: {global_document_id_index}/{len(global_document_ids) - 1}')
        return global_document_ids[global_document_id_index]


def get_run_and_document(run_document_id: str) -> Union[Tuple[Run, Document], None]:
    run_id, document_id = (int(str_id) for str_id in run_document_id.split(sep='|'))
    if run := get_orbis_service().get_run(run_id):
        document = [document for document in run.document_annotations.keys() if document.document_id == document_id][0]
        return run, document
    return None


@app.get('/getCorpora', response_model=ResponseModel)
def get_corpora():
    if corpora := get_orbis_service().get_corpora():
        response = Response(status_code=200,
                            content={'corpora': [corpus.name for corpus in corpora]},
                            message=f'Found {len(corpora)} corpora in db.')
    else:
        response = Response(status_code=400,
                            message='No corpora found.')
    return response.as_json()


@app.get('/getDocumentsOfCorpus', response_model=ResponseModel)
def get_documents_of_corpus(corpus_name=None):
    if not corpus_name:
        response = Response(status_code=400,
                            message='No corpus name provided. Try again with e.g. '
                                    '/getDocumentsOfCorpus?corpus_name=your_corpus_name')
    elif ((corpus_id := get_orbis_service().get_corpus_id(corpus_name)) and
          (runs := get_orbis_service().get_runs_by_corpus_id(corpus_id))):
        run = runs[0]
        documents = list(run.document_annotations.keys())
        response = Response(status_code=200,
                            content={'corpora': [{'da_id': run.run_id.__str__() + '|' + document.document_id.__str__(),
                                                  'd_id': document.document_id,
                                                  'annotator': 'new_orbis2',
                                                  'last_edited': '2022-01-01 00:00:00'} for document in documents]},
                            message=f'Found {len(documents)} documents in corpus {corpus_name}.')
    else:
        response = Response(status_code=400,
                            message='No corpora found.')
    return response.as_json()


@app.get('/getDocumentForAnnotation', response_model=ResponseModel)
def get_document_for_annotation(corpus_name=None, annotator=None):
    run_document_id = get_document_id(1)
    return get_document(run_document_id)


@app.get('/getNextDocumentForAnnotation', response_model=ResponseModel)
def get_next_document_for_annotation(index):
    run_document_id = get_document_id(index)
    return get_document(run_document_id)


@app.get('/getCurrentIndexState', response_model=ResponseModel)
def get_current_index_state():
    global global_document_ids
    global global_document_id_index
    has_next_document = (global_document_ids and global_document_id_index < len(global_document_ids) - 1)
    has_previous_document = (global_document_ids and global_document_id_index > 0)
    response = Response(status_code=200,
                        content={'has_next_document': has_next_document,
                                 'has_previous_document': has_previous_document})
    return response.as_json()


@app.get('/getDocument', response_model=ResponseModel)
def get_document(da_id=None):
    response = Response(status_code=400,
                        message='No corpora found.')
    if da_id:
        if run_document := get_run_and_document(da_id):
            run, document = run_document
            annotations = run.document_annotations[document]
            response = Response(
                status_code=200,
                content={
                    'da_id': da_id,
                    'text': document.content,
                    'annotations': {
                        'd_id': document.document_id,
                        'meta': '',
                        'annotations': [{
                            'key': annotation.key,
                            'type': annotation.annotation_type.name + "-" + annotation.key.split('#')[1].replace('/', '')
                            if annotation.annotation_type.name == 'proposal' else annotation.annotation_type.name,
                            'surface_form': annotation.surface_forms[0],
                            'start': annotation.start_indices[0],
                            'end': annotation.end_indices[0],
                            'scope': '',
                            'meta': {}
                        } for annotation in annotations]
                    }
                }
            )
    return response.as_json()


@app.post('/saveDocumentAnnotations', response_model=ResponseModel)
def save_document_annotations(data: DataExchangeModel):
    data = data.dict()
    da_id = data.get('da_id')
    if run_document := get_run_and_document(da_id):
        run, document = run_document
        annotations = [Annotation(f"https://semanticlab.net/career-coach#{annotation.get('type').split('-')[1]}/" if 'proposal' in annotation.get('type') else annotation.get('key'),
                                  annotation.get('surface_form'), annotation.get('start'),
                                  annotation.get('end'), AnnotationType(annotation.get('type').split('-')[0]),
                                  Annotator(data.get('annotator'), []), metadata=[Metadata('segment', 'unknown')])
                       for annotation in data.get('data').get('annotations')]
        run.document_annotations[document] = annotations
        if get_orbis_service().add_run(run):
            response = Response(status_code=200,
                                content={'da_id': da_id})
        else:
            response = Response(status_code=400,
                                message=f'Document Annotation not saved in db for da: {da_id}')
        return response.as_json()


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63019)
