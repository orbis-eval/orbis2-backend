import datetime
from typing import Union, Tuple

from orbis2.database.orbis.entities.annotation_dao import AnnotationDao
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.metadata import Metadata


class Annotation:
    """
    Mock Annotation class used within the unittests.
    """

    def __init__(self, key: str, surface_forms: Union[Tuple[str, ...], str], start_indices: Union[Tuple[int, ...], int],
                 end_indices: Union[Tuple[int, ...], int], annotation_type: AnnotationType, annotator: Annotator,
                 run_id, document_id, metadata: [Metadata] = None, timestamp: datetime = None):
        if isinstance(start_indices, int):
            start_indices = (start_indices, )
        if isinstance(end_indices, int):
            end_indices = (end_indices, )
        if isinstance(surface_forms, str):
            surface_forms = (surface_forms, )

        self.annotation_id = None
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

    @classmethod
    def from_annotation_dao(cls, annotation_dao: AnnotationDao, run_id: int, document_id: int,
                            timestamp: datetime) -> 'Annotation':
        annotation = cls(annotation_dao.key, annotation_dao.surface_forms, annotation_dao.start_indices,
                         annotation_dao.end_indices,
                         AnnotationType.from_annotation_type_dao(annotation_dao.annotation_type),
                         Annotator.from_annotator_dao(annotation_dao.annotator), run_id, document_id,
                         Metadata.from_metadata_daos(annotation_dao.meta_data), timestamp)
        annotation.annotation_id = annotation_dao.annotation_id
        return annotation

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __len__(self):
        return sum((end - start for start, end in zip(self.start, self.end)))

    def __gt__(self, other):
        return self.start[0] >= other.start[0] or \
               (self.start[0] == other.start[0] and
                self.end[-1] >= other.end[-1])

    def __lt__(self, other):
        return not self.__gt__(other)

    def __hash__(self):
        return hash((self.start, self.end))

    def __str__(self):
        return f'Annotation({self.start}, {self.end})'

    def __repr__(self):
        return self.__str__()
