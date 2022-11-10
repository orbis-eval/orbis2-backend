from orbis2.database.orbis.entities.annotation_type_dao import AnnotationTypeDao


class AnnotationType:

    def __init__(self, name: str):
        """
        CONSTRUCTOR

        """
        self.type_id = None
        self.name = name

    @classmethod
    def from_annotation_type_dao(cls, annotation_type_dao: AnnotationTypeDao) -> 'AnnotationType':
        annotation_type = cls(annotation_type_dao.name)
        annotation_type.type_id = annotation_type_dao.type_id
        return annotation_type

    @classmethod
    def from_annotation_type_daos(cls, annotation_type_daos: [AnnotationTypeDao]) -> ['AnnotationType']:
        annotation_types = []
        for annotation_type_dao in annotation_type_daos:
            annotation_types.append(AnnotationType.from_annotation_type_dao(annotation_type_dao))
        return annotation_types
