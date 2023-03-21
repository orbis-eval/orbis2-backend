import logging

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

from orbis2.database.session import get_session


class SqlDb:
    """
    The interface containing all the necessary database logic.

    Attributes
        url: database url to set up the session
        _session: running session to the database, given by the url in the constructor.

    """

    def __init__(self, url: str, base):
        """
        CONSTRUCTOR

        Attributes:
            url: database url to set up the session
            base: declarative base contains all the necessary database metadata (schema, tables, etc.)

        """
        self.url = url
        self.base = base
        try:
            self._session = get_session(self.url)
        except SQLAlchemyError as e:
            logging.error(f'Session could not be initialized, exception: {e.__str__()}')

    @property
    def session(self):
        try:
            # check whether database connection is working properly
            self._session.execute(text('SELECT 1'))
        except DBAPIError:
            logging.info(f'Lost DB connection ({self.__class__.__name__}), reconnect...')
            self._session = get_session(self.url, True)
        return self._session

    def __del__(self):
        """
        DESTRUCTOR

        """
        try:
            self._session.close()
        except SQLAlchemyError as e:
            logging.error(f'Session could not be closed, exception: {e.__str__()}')

    def commit(self) -> bool:
        """
        Database commit, necessary after data insert.

        """
        try:
            self._session.commit()
            return True
        except SQLAlchemyError as e:
            self._session.rollback()
            logging.error(f'During committing the following exception occurred: {e.__str__()}')
            return False

    def create_database(self, enforce: bool = False) -> bool:
        """
        Create recommender database scheme if not already existing and create/clear recommender tables.

        Returns: True if database exists after creation.
        """
        # try:
        if not database_exists(self.session.get_bind().url):
            create_database(self.session.get_bind().url)
        elif enforce:
            self.clear_tables()
        else:
            logging.warning('Database already exists, if you want to reinitialize it, set enforce = True '
                            '(ATTENTION: data will be lost)')
            return False
        return database_exists(self.session.get_bind().url)
        # except SQLAlchemyError as e:
        #     logging.error(f'During database creation the following exception occurred: {e.__str__()}')
        #     return False

    def clear_tables(self) -> bool:
        """
        Clear all tables, dropping and recreating is the easiest way in sqlalchemy.

        Returns: True if everything worked correctly.
        """
        try:
            self.base.metadata.drop_all(self.session.get_bind())
            self.base.metadata.create_all(self.session.get_bind())
            return True
        except SQLAlchemyError as e:
            logging.error(f'During clearing the tables the following exception occurred: {e.__str__()}')
            return False
