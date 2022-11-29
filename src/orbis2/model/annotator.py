from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.model.base_model import BaseModel
from orbis2.model.role import Role


class Annotator(BaseModel):

    def __init__(self, name: str, roles: [Role]):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.roles = roles

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Annotator):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_annotator_dao(cls, annotator_dao: AnnotatorDao):
        annotator = cls(annotator_dao.name, Role.from_role_daos(annotator_dao.roles))
        if annotator_dao.annotator_id:
            annotator.annotator_id = annotator_dao.annotator_id
        return annotator

    def to_dao(self) -> AnnotatorDao:
        return AnnotatorDao(annotator_id=self.get_id(), name=self.name, roles=Role.to_role_daos(self.roles))
