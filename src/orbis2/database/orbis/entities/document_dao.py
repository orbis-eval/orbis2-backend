from sqlalchemy import Sequence, BigInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped

from orbis2.database.orbis.entities.document_has_metadata_relation import document_has_metadata_table
from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.database.orbis.orbis_base import OrbisBase


class DocumentDao(OrbisBase):
    __tablename__ = 'document'

    document_id: Mapped[int] = mapped_column(BigInteger, Sequence('document_id_seq'), primary_key=True)
    content: Mapped[str]
    key: Mapped[str] = mapped_column(default='')
    meta_data: Mapped[MetadataDao] = relationship(secondary=document_has_metadata_table)

    # TODO, anf 23.03.2023: to_tsvector is deprecated in SQLAlchemy2.0,
    #  it has been used for indexing the content of a document for faster full string search
    # __table_args__ = (
    #     # ',' after Index(), is necessary, since the value of table_args must be a tuple, dictionary, or None
    #     Index(
    #         'document_text_idx',
    #         to_tsvector('english', content),
    #         postgresql_using='gin'
    #     ),
    # )
