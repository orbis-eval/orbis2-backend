from sqlalchemy import Column, Integer, Sequence, VARCHAR

from src.database.orbis.orbis_base import OrbisBase


class AnnotatorDao(OrbisBase):
    __tablename__ = 'annotator'

    annotator_id = Column(Integer, Sequence('annotator_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
