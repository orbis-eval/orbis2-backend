from dataclasses import dataclass
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.model.base_model import BaseModel


@dataclass
class Metadata(BaseModel):
    key: str
    value: str
    id: int  # noqa: A003

    def __init__(self, key: str, value: str):
        """
        CONSTRUCTOR

        """
        self.key = key
        self.value = value

    def __hash__(self):
        return xxh32_intdigest(self.key + self.value)

    def __eq__(self, other):
        if isinstance(other, Metadata):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_metadata_dao(cls, metadata_dao: MetadataDao) -> 'Metadata':
        metadata = cls(metadata_dao.key, metadata_dao.value)
        return metadata

    @classmethod
    def from_metadata_daos(cls, metadata_daos: [MetadataDao]) -> ['Metadata']:
        return [cls.from_metadata_dao(metadata_dao) for metadata_dao in metadata_daos]

    def to_dao(self) -> MetadataDao:
        return MetadataDao(metadata_id=self.id, key=self.key, value=self.value)

    @staticmethod
    def to_metadata_daos(metadata: ['Metadata']) -> [MetadataDao]:
        return [metadata.to_dao() for metadata in metadata]

    def __str__(self):
        return f'<Metadata: {self.key}: {self.value}>'

    def __repr__(self):
        return self.__str__()

    def copy(self) -> 'Metadata':
        return Metadata(self.key, self.value)
