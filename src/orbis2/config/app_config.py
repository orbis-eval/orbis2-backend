import os
from pathlib import Path


class AppConfig:
    """
    Contains the configuration which can be set via the environment variables.
    If the environment variable is not present at startup of the application,
    a default value is used.
    """

    @staticmethod
    def get_db_url() -> str:
        """
        Returns: Url which is used to access the database.
        """
        if not (db_url := os.getenv('DB_URL')):
            db_url = 'localhost'
        return db_url

    @staticmethod
    def get_db_port() -> str:
        """
        Returns: Port which is used to access the database.
        """
        if not (db_port := os.getenv('DB_PORT')):
            db_port = '5432'
        return db_port

    @staticmethod
    def get_db_user() -> str:
        """
        Returns: User which is used to access the database.
        """
        if not (db_user := os.getenv('DB_USER')):
            db_user = 'postgres'
        return db_user

    @staticmethod
    def get_db_password() -> str:
        """
        Returns: Password which is used to access the database.
        """
        if not (db_password := os.getenv('DB_PASSWORD')):
            return ''
        return db_password

    @staticmethod
    def get_orbis_db_name() -> str:
        """
        Returns: Name of the orbis database which is used to access the database.
        """
        if not (db_name := os.getenv('ORBIS_DB_NAME')):
            db_name = 'orbis'
        return db_name

    @staticmethod
    def get_orbis_db_url() -> str:
        """
        Returns: Url of the orbis database which is used to access the database.
        """
        return f'postgresql://{AppConfig.get_db_user()}:{AppConfig.get_db_password()}@' \
               f'{AppConfig.get_db_url()}:{AppConfig.get_db_port()}/{AppConfig.get_orbis_db_name()}'

    @staticmethod
    def get_logging_config_path() -> str:
        """
        Returns: Absolute path to the logger.ini file for the logging configuration.
        """
        return f'{Path(__file__).parents[3]}/config/logger.ini'
