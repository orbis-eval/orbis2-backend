from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from xxhash import xxh3_64_intdigest, xxh32_intdigest


class AnnotationType:

    __slots__ = ('name', 'type_id')

    def __init__(self, name: str):
        """
        CONSTRUCTOR

        """
        self.name = name
        self.type_id = self.__hash__()

    def __hash__(self):
        return xxh32_intdigest(self.name)

    def __eq__(self, other):
        if isinstance(other, AnnotationType):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_annotation_type_dao(cls, annotation_type_dao: AnnotationTypeDao) -> 'AnnotationType':
        annotation_type = cls(annotation_type_dao.name)
        if annotation_type_dao.type_id:
            annotation_type.type_id = annotation_type_dao.type_id
        return annotation_type

    @classmethod
    def from_annotation_type_daos(cls, annotation_type_daos: [AnnotationTypeDao]) -> ['AnnotationType']:
        return [cls.from_annotation_type_dao(annotation_type_dao)
                for annotation_type_dao in annotation_type_daos]

    def to_dao(self) -> AnnotationTypeDao:
        return AnnotationTypeDao(type_id=self.type_id, name=self.name)

    @staticmethod
    def to_annotation_type_daos(annotation_types: ['AnnotationType']) -> [AnnotationTypeDao]:
        return [annotation_type.to_dao() for annotation_type in annotation_types]
