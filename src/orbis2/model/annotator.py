from typing import List

from xxhash import xxh32_intdigest, xxh32_hexdigest

from orbis2.database.orbis.entities.annotator_dao import AnnotatorDao
from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.role import Role


class Annotator(OrbisPydanticBaseModel):
    name: str
    roles: List[Role]
    password: str = xxh32_hexdigest('')

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Annotator):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_annotator_dao(cls, annotator_dao: AnnotatorDao) -> 'Annotator':
        annotator = cls(name=annotator_dao.name, roles=Role.from_role_daos(annotator_dao.roles),
                        password=annotator_dao.password)
        return annotator

    @classmethod
    def from_annotator_daos(cls, annotator_daos: [AnnotatorDao]) -> ['Annotator']:
        return [cls.from_annotator_dao(annotator_dao) for annotator_dao in annotator_daos]

    def to_dao(self) -> AnnotatorDao:
        return AnnotatorDao(annotator_id=self._id, name=self.name, password=self.password,
                            roles=Role.to_role_daos(self.roles))
