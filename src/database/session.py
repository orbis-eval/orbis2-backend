from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sessions_makers = {}


def get_session(connection_string: str, new: bool = False) -> Session:
    """
    Returns a sqlalchemy session for the connection string
    Args:
        connection_string: connection string for sqlalchemy for connecting to the database
        new: if true, remove the existing session and create a new one

    Returns: sqlalchemy session
    """
    if new:
        sessions_makers.pop(connection_string)
    if connection_string not in sessions_makers:
        engine = create_engine(connection_string, echo=True)
        sessions_makers[connection_string] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return sessions_makers[connection_string]()
