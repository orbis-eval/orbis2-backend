import logging.config
from pathlib import Path

from src.config.app_config import AppConfig
from src.database.orbis.orbis_db import OrbisDb


LOGGING_DIR = Path(__file__).parents[0] / 'log'
LOGGING_DIR.mkdir(exist_ok=True)
logging.config.fileConfig(AppConfig.get_logging_config_path(), disable_existing_loggers=False)

if __name__ == '__main__':
    print(OrbisDb().create_database())
    # print(OrbisDb().get_annotations())
