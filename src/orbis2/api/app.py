import logging.config
import sys
import threading

import uvicorn as uvicorn
from fastapi import FastAPI

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.config.app_config import AppConfig
from orbis2.metadata import __version__
from pathlib import Path

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


def get_orbis_service() -> OrbisService:
    global global_orbis_service
    with ORBIS_SERVICE_LAZY_INIT_LOCK:
        if not global_orbis_service:
            global_orbis_service = OrbisService()
        return global_orbis_service


@app.get('/getCorpus/{corpus_id}', response_model=Run)
def save_document_annotations(corpus_id: int):
    runs = get_orbis_service().get_runs_by_corpus_id(corpus_id)
    return runs[0]


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=63019)
