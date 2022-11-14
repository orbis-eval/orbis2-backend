import logging.config
import sys
import threading

import uvicorn as uvicorn
from fastapi import FastAPI

from orbis2.api.model.deprecated.response import Response
from orbis2.api.model.deprecated.response_model import ResponseModel
from orbis2.business_logic.orbis_service import OrbisService
from orbis2.config.app_config import AppConfig
from orbis2.metadata import __version__
from pathlib import Path

# getDocumentsOfCorpus
# getCorpora
# getDocumentForAnnotation
# getDocument
# saveDocumentAnnotations

PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

LOGGING_DIR = PROJECT_DIR / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

ORBIS_SERVICE_LAZY_INIT_LOCK = threading.Lock()

app = FastAPI(
    title='Orbis2 Backend',
    version=__version__
)

global_orbis_service = None


def get_orbis_service():
    global global_orbis_service
    with ORBIS_SERVICE_LAZY_INIT_LOCK:
        if not global_orbis_service:
            global_orbis_service = OrbisService()
        return global_orbis_service


# @app.get('/getDocumentForAnnotation', response_model=ResponseModel)
# async def get_document_for_annotation(corpus_name=None, annotator=None):
#     logging.info(f'get_document_for_annotation with corpus "{corpus_name}" and annotator "{annotator}"')
#     if da_id := await annotator_queue.get_id_for_annotation(corpus_name, annotator):
#         return await get_document(da_id)
#     else:
#         response = Response(status_code=400,
#                             message='Empty annotator queue for request.',
#                             content={'corpus_name': corpus_name, 'annotator': annotator})
#     return response.as_json()


@app.get('/getDocumentsOfCorpus', response_model=ResponseModel)
def get_documents_of_corpus(corpus_name=None):
    if not corpus_name:
        response = Response(status_code=400,
                            message='No corpus name provided. Try again with e.g. '
                                    '/getDocumentsOfCorpus?corpus_name=your_corpus_name')
    elif ((corpus_id := get_orbis_service().get_corpus_id(corpus_name)) and
          (runs := get_orbis_service().get_runs_by_corpus_id(corpus_id))):
        documents = list(runs[0].document_annotations.keys())
        response = Response(status_code=200,
                            # TODO, anf 14.11.2022: correctly transform documents into expected response format
                            content={'corpora': documents},
                            message=f'Found {len(documents)} documents in corpus {corpus_name}.')
    else:
        response = Response(status_code=400,
                            message='No corpora found.')
    return response.as_json()


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63019)
