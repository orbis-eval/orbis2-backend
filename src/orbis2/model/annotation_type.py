from xxhash import xxh3_64_intdigest

from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao


class AnnotationType:

    def __init__(self, name: str):
        """
        CONSTRUCTOR

        """
        self.type_id = xxh3_64_intdigest(name)
        self.name = name

    @classmethod
    def from_annotation_type_dao(cls, annotation_type_dao: AnnotationTypeDao) -> 'AnnotationType':
        annotation_type = cls(annotation_type_dao.name)
        annotation_type.type_id = annotation_type_dao.type_id
        return annotation_type

    @classmethod
    def from_annotation_type_daos(cls, annotation_type_daos: [AnnotationTypeDao]) -> ['AnnotationType']:
        return [AnnotationType.from_annotation_type_dao(annotation_type_dao)
                for annotation_type_dao in annotation_type_daos]

    def to_dao(self) -> AnnotationTypeDao:
        return AnnotationTypeDao(type_id=self.type_id, name=self.name)

    @staticmethod
    def to_annotation_type_daos(annotation_types: ['AnnotationType']) -> [AnnotationTypeDao]:
        return [annotation_type.to_dao() for annotation_type in annotation_types]
