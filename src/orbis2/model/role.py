from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.role_dao import RoleDao


class Role:

    def __init__(self, name: str):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.role_id = self.__hash__()

    def __hash__(self):
        return xxh32_intdigest(self.name)

    @classmethod
    def from_role_dao(cls, role_dao: RoleDao) -> 'Role':
        role = cls(role_dao.name)
        if role_dao:
            role.role_id = role_dao.role_id
        return role

    @classmethod
    def from_role_daos(cls, role_daos: [RoleDao]) -> ['Role']:
        return [Role.from_role_dao(role_dao) for role_dao in role_daos]

    def to_dao(self) -> RoleDao:
        return RoleDao(role_id=self.role_id, name=self.name)

    @staticmethod
    def to_role_daos(roles: [RoleDao]) -> [RoleDao]:
        return [role.to_dao() for role in roles]