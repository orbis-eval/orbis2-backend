from dataclasses import dataclass
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao
from orbis2.model.base_model import BaseModel


@dataclass
class AnnotationType(BaseModel):
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
        if isinstance(other, AnnotationType):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_annotation_type_dao(cls, annotation_type_dao: AnnotationTypeDao) -> 'AnnotationType':
        annotation_type = cls(annotation_type_dao.name)
        return annotation_type

    @classmethod
    def from_annotation_type_daos(cls, annotation_type_daos: [AnnotationTypeDao]) -> ['AnnotationType']:
        return [cls.from_annotation_type_dao(annotation_type_dao)
                for annotation_type_dao in annotation_type_daos]

    def to_dao(self) -> AnnotationTypeDao:
        return AnnotationTypeDao(type_id=self.id, name=self.name)

    @staticmethod
    def to_annotation_type_daos(annotation_types: ['AnnotationType']) -> [AnnotationTypeDao]:
        return [annotation_type.to_dao() for annotation_type in annotation_types]

    def copy(self) -> 'AnnotationType':
        return AnnotationType(self.name)
