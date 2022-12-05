import argparse
import json
import logging.config
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'src'))

from orbis2.config.app_config import AppConfig

LOGGING_DIR = PROJECT_DIR / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path())
logger = logging.getLogger(__name__)

from orbis2.api.app import get_app

parser = argparse.ArgumentParser()
parser.add_argument('-fn', '--filename', help='How the output file should be named')
args = parser.parse_args()

filename = 'openapi.json'

if __name__ == '__main__':
    app = get_app()
    if args.filename:
        filename = args.filename

    with open(Path(__file__).parent / filename, 'w+') as file:
        json.dump(app.openapi(), file)
