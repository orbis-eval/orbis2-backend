from sqlalchemy import Integer, Sequence, Column, Text
from sqlalchemy.orm import relationship

from orbis2.database.orbis.orbis_base import OrbisBase


class RoleDao(OrbisBase):
    __tablename__ = 'role'

    role_id = Column(Integer, Sequence('role_id_seq'), primary_key=True)
    name = Column(Text, nullable=False)
    annotators = relationship('AnnotatorDao', secondary='annotator_has_role', back_populates='roles')
