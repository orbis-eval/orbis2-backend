import sys
import threading
from pathlib import Path
from typing import List
from datetime import datetime
import json

import uvicorn as uvicorn
from fastapi import FastAPI, Response, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.metadata import __version__
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.run import Run
from orbis2.model.gold_standard import GoldStandard

from orbis2.evaluation.helper import get_inter_rater_agreement_result

from orbis2.corpus_import.format.tools.helper_importer import HelperImporter

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
    version=__version__,
    default_response_class=ORJSONResponse
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:63012",
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


def get_error_response(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(content={"message": message}, status_code=status_code)


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
def get_document(run_id: int, document_id: int) -> Document:
    return get_orbis_service().get_document(run_id, document_id)


@app.get('/getRuns')
def get_runs(corpus_id: int = None) -> List[Run]:
    if corpus_id:
        runs = get_orbis_service().get_run_names(corpus_id)
    else:
        runs = get_orbis_service().get_run_names()

    # @todo pydantic bug: cant handle dicts, therefore setting document_annotations to None
    for run in runs:
        run.document_annotations = None
        if run.current_gold_standard:
            run.current_gold_standard.document_annotations = None

    return runs


@app.get('/getGoldStandards')
def get_gold_standards(corpus_id: int = None) -> List[GoldStandard]:
    if corpus_id:
        gold_standards = get_orbis_service().get_gold_standard_names(corpus_id)
    else:
        gold_standards = get_orbis_service().get_gold_standard_names()

    # @todo pydantic bug: cant handle dicts, therefore setting document_annotations to None
    for gold_standard in gold_standards:
        gold_standard.document_annotations = None
        if gold_standard.current_gold_standard:
            gold_standard.current_gold_standard.document_annotations = None
    return gold_standards


@app.get('/getCorpora')
def get_corpora() -> List[Corpus]:
    return get_orbis_service().get_corpora()


@app.get('/getCorpus')
def get_corpus(corpus_id: int) -> Corpus:
    return get_orbis_service().get_corpus(corpus_id)


@app.post('/createCorpus', status_code=201)
def create_corpus(corpus: Corpus, file: dict = None) -> Corpus:
    try:
        documents_with_annotations_list, annotation_types = HelperImporter.get_annotated_documents_and_types(file)
    except json.JSONDecodeError as e:
        return get_error_response(f"Failed to parse file content: {str(e)}", status.HTTP_400_BAD_REQUEST)

    documents_with_annotations_dict = {}
    corpus.supported_annotation_types = [AnnotationType(annotation_type) for annotation_type in annotation_types]

    for pair in documents_with_annotations_list:
        document, annotations = pair
        documents_with_annotations_dict[document] = annotations

    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    run = Run(
        'gold_standard_' + current_timestamp, f'default run for corpus {corpus.name}, no annotations',
        corpus,
        documents_with_annotations_dict,
        is_gold_standard=True
    )
    get_orbis_service().add_run(run)
    return corpus


@app.post('/createRun', status_code=201)
def create_run(corpus: Corpus, run_name: str, file: dict) -> Run:
    if corpus and run_name and file:
        documents_with_annotations_list, annotation_types = HelperImporter.get_annotated_documents_and_types(file)
        documents_with_annotations_dict = {}
        documents_of_corpus = get_orbis_service().get_documents_of_corpus(corpus.identifier)

        for corpus_document in documents_of_corpus:
            for pair in documents_with_annotations_list:
                document, annotations = pair
                if corpus_document.__hash__() == document.__hash__():
                    documents_with_annotations_dict[document] = annotations

        run_name = run_name + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        run = Run(run_name, "Run description", corpus, documents_with_annotations_dict)

        gold_standards = get_orbis_service().get_run_names(corpus.identifier, is_gold_standard=True)
        last_gold_standard = gold_standards[0] if gold_standards else None
        if last_gold_standard:
            run.current_gold_standard = last_gold_standard
            try:
                run.inter_rater_agreement = get_inter_rater_agreement_result(
                    last_gold_standard.document_annotations, run.document_annotations)
            except Exception as e:
                return get_error_response(f"Failed to calculate inter-rater agreement: {str(e)}",
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)

        if get_orbis_service().add_run(run):
            run.document_annotations = None
            run.current_gold_standard.document_annotations = {}
            return run
    return get_error_response("Failed to create run.", status.HTTP_400_BAD_REQUEST)


@app.post('/updateGoldStandard', status_code=201)
def update_gold_standard(corpus: Corpus, file: dict) -> Run:
    if corpus and file:
        documents_with_annotations_list, annotation_types = HelperImporter.get_annotated_documents_and_types(file)
        documents_with_annotations_dict = {}

        corpus.supported_annotation_types = [AnnotationType(annotation_type) for annotation_type in annotation_types]

        for pair in documents_with_annotations_list:
            document, annotations = pair
            documents_with_annotations_dict[document] = annotations

        current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        run = Run("gold_standard_" + current_timestamp, "", corpus, documents_with_annotations_dict,
                  is_gold_standard=True)

        if get_orbis_service().add_run(run):
            run.document_annotations = None
            return run
    return get_error_response("Failed to update gold standard.", status.HTTP_400_BAD_REQUEST)


def validate_corpus_id(corpus_id: int) -> None:
    if not corpus_id:
        raise ValueError(f"Corpus {corpus_id} has no corpus id.")


def validate_run_count(corpus_id: int) -> None:
    run_names = get_orbis_service().get_run_names(corpus_id)
    if len(run_names) <= 1:
        raise ValueError(f"Corpus {corpus_id} must have at least two runs.")


@app.delete('/deleteRun', status_code=200)
def delete_run(run: Run) -> {}:
    try:
        validate_corpus_id(run.corpus.identifier)
        validate_run_count(run.corpus.identifier)

        if get_orbis_service().delete_run(run.identifier):
            message = f"Run with ID {run.identifier} has been deleted successfully."
            return JSONResponse(content={"message": message})
        else:
            return get_error_response(f"Failed to delete Run with ID {run.identifier}.",
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as e:
        return get_error_response(str(e), status.HTTP_400_BAD_REQUEST)


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
    if get_orbis_service().delete_corpus(corpus.identifier):
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
