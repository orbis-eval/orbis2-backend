from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.model.role import Role


class Annotator:

    def __init__(self, name: str, roles: [Role]):
        """
        CONSTRUCTOR

        """
        self.annotator_id = None
        self.name = name
        self.roles = roles

    @classmethod
    def from_annotator_dao(cls, annotator_dao: AnnotatorDao):
        annotator = cls(annotator_dao.name, Role.from_role_daos(annotator_dao.roles))
        annotator.annotator_id = annotator_dao.annotator_id
        return annotator
