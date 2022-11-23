import datetime
from typing import Union, Tuple, List

from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata


class Annotation:
    """
    Mock Annotation class used within the unittests.
    """

    def __init__(self, key: str, surface_forms: Union[Tuple[str, ...], str],
                 start_indices: Union[Tuple[int, ...], int],
                 end_indices: Union[Tuple[int, ...], int],
                 annotation_type: AnnotationType, annotator: Annotator,
                 run_id: int = None, document_id: int = None,
                 metadata: [Metadata] = None, timestamp: datetime = None):
        if isinstance(start_indices, int):
            start_indices = (start_indices, )
        if isinstance(start_indices, List):
            start_indices = tuple(start_indices)
        if isinstance(end_indices, int):
            end_indices = (end_indices, )
        if isinstance(end_indices, List):
            end_indices = tuple(end_indices)
        if isinstance(surface_forms, str):
            surface_forms = (surface_forms, )
        if isinstance(surface_forms, List):
            surface_forms = tuple(surface_forms)

        self.key = key
        self.surface_forms = surface_forms
        self.start_indices = start_indices
        self.end_indices = end_indices
        self.annotation_type = annotation_type
        self.annotator = annotator
        self.run_id = run_id
        self.document_id = document_id
        self.metadata = metadata if metadata else []
        self.timestamp = timestamp
        self.annotation_id = self.__hash__()

    def __eq__(self, other):
        if isinstance(other, Annotation):
            return self.__hash__() == other.__hash__()
        return False

    def __len__(self):
        return sum((end - start for start, end in zip(
            self.start_indices, self.end_indices)))

    def __gt__(self, other):
        return self.start_indices[0] >= other.start_indices[0] or \
               (self.start_indices[0] == other.start_indices[0] and
                self.end_indices[-1] >= other.end_indices[-1])

    def __lt__(self, other):
        return not self.__gt__(other)

    def __hash__(self):
        return xxh32_intdigest((self.key, self.surface_forms, self.start_indices, self.end_indices,
                                self.annotation_type.__hash__(), self.annotator.__hash__()).__str__())

    def __str__(self):
        return f'Annotation({self.surface_forms}{self.start_indices}, {self.end_indices})'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_annotation_dao(cls, annotation_dao: AnnotationDao, run_id: int, document_id: int,
                            timestamp: datetime) -> 'Annotation':
        annotation = cls(annotation_dao.key, annotation_dao.surface_forms, annotation_dao.start_indices,
                         annotation_dao.end_indices,
                         AnnotationType.from_annotation_type_dao(annotation_dao.annotation_type),
                         Annotator.from_annotator_dao(annotation_dao.annotator), run_id, document_id,
                         Metadata.from_metadata_daos(annotation_dao.meta_data), timestamp)
        if annotation_dao.annotator_id:
            annotation.annotation_id = annotation_dao.annotation_id
        return annotation

    def to_dao(self) -> AnnotationDao:
        return AnnotationDao(annotation_id=self.annotation_id, key=self.key,
                             surface_forms=list(self.surface_forms),
                             start_indices=list(self.start_indices),
                             end_indices=list(self.end_indices),
                             annotation_type=self.annotation_type.to_dao(),
                             annotator=self.annotator.to_dao(),
                             meta_data=Metadata.to_metadata_daos(self.metadata))


def get_mock_annotation(start_indices: Union[Tuple[int, ...], int],
                        end_indices: Union[Tuple[int, ...], int],
                        surface_forms: Union[Tuple[str, ...], str] = None,
                        key: str = "mock",
                        metadata: [Metadata] = None):
    """
    Return:
         A mock Annotation to be used in unittests.
    """
    return Annotation(key=key,
                      surface_forms=surface_forms,
                      start_indices=start_indices,
                      end_indices=end_indices,
                      annotation_type=None,
                      annotator=None,
                      metadata=metadata)
