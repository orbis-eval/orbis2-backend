from sqlalchemy import Column, Sequence, BigInteger, Text, Index
from sqlalchemy.sql import func

from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentDao(OrbisBase):
    __tablename__ = 'document'

    document_id = Column(BigInteger, Sequence('document_id_seq'), primary_key=True)
    content = Column(Text, nullable=False)

    __table_args__ = (
        # ',' after Index(), is necessary, since the value of table_args must be a tuple, dictionary, or None
        Index(
            'document_text_idx',
            func.to_tsvector('english', content),
            postgresql_using='gin'
        ),
    )
