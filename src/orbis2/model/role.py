from orbis2.database.orbis.entities.role_dao import RoleDao


class Role:

    def __init__(self, name: str):
        """
        CONSTRUCTOR

        """
        self.role_id = None
        self.name = name

    @classmethod
    def from_role_dao(cls, role_dao: RoleDao) -> 'Role':
        role = cls(role_dao.name)
        role.role_id = role_dao.role_id
        return role

    @classmethod
    def from_role_daos(cls, role_daos: [RoleDao]) -> ['Role']:
        roles = []
        for role_dao in role_daos:
            roles.append(Role.from_role_dao(role_dao))
        return roles
