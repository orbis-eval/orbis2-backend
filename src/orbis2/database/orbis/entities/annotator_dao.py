from sqlalchemy import Column, Sequence, VARCHAR, BigInteger
from sqlalchemy.orm import relationship

from orbis2.database.orbis.entities.annotator_has_role_relation import annotator_has_role_table
from orbis2.database.orbis.orbis_base import OrbisBase


class AnnotatorDao(OrbisBase):
    __tablename__ = 'annotator'

    annotator_id = Column(BigInteger, Sequence('annotator_id_seq'), primary_key=True)
    name = Column(VARCHAR(40), nullable=False)
    password = Column(VARCHAR(50))
    roles = relationship('RoleDao', secondary=annotator_has_role_table)
