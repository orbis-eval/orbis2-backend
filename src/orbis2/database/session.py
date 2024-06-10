from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sessions_makers = {}

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def get_session(connection_string: str, new: bool = False) -> Session:
    """
    Returns a sqlalchemy session for the connection string
    Args:
        connection_string: connection string for sqlalchemy for connecting to the database
        new: if true, delete the existing session and create a new one

    Returns: sqlalchemy session
    """
    if new:
        sessions_makers.pop(connection_string, None)  # Use pop with default value to avoid KeyError
    if connection_string not in sessions_makers:
        # Configure the engine with connection pooling options
        engine = create_engine(
            connection_string,
            pool_size=20,  # Maximum number of connections in the pool
            max_overflow=10,  # Maximum number of connections to open beyond pool_size
            pool_timeout=30,  # Maximum time to wait for a connection to become available
            pool_recycle=1800  # Time (in seconds) after which connections will be recycled
        )
        sessions_makers[connection_string] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return sessions_makers[connection_string]()
