from dataclasses import dataclass
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.role_dao import RoleDao
from orbis2.model.base_model import BaseModel


@dataclass
class Role(BaseModel):
    name: str
    _id: int

    def __init__(self, name: str, _id: int = 0):
        """
        CONSTRUCTOR

        """
        self.name = name

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, Role):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_role_dao(cls, role_dao: RoleDao) -> 'Role':
        role = cls(role_dao.name)
        return role

    @classmethod
    def from_role_daos(cls, role_daos: [RoleDao]) -> ['Role']:
        return [cls.from_role_dao(role_dao) for role_dao in role_daos]

    def to_dao(self) -> RoleDao:
        return RoleDao(role_id=self._id, name=self.name)

    @staticmethod
    def to_role_daos(roles: [RoleDao]) -> [RoleDao]:
        return [role.to_dao() for role in roles]

    def copy(self) -> 'Role':
        return Role(self.name)
