from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.metadata_dao import MetadataDao
from orbis2.model.base_model import OrbisPydanticBaseModel


class Metadata(OrbisPydanticBaseModel):
    key: str
    value: str
    
    def __init__(self, key: str, value: str):
        super().__init__(key=key, value=value)

    def __hash__(self):
        return xxh32_intdigest(self.key + self.value)

    def __eq__(self, other):
        if isinstance(other, Metadata):
            return self.__hash__() == other.__hash__()
        return False

    @classmethod
    def from_metadata_dao(cls, metadata_dao: MetadataDao) -> 'Metadata':
        metadata = cls(key=metadata_dao.key, value=metadata_dao.value)
        return metadata

    @classmethod
    def from_metadata_daos(cls, metadata_daos: [MetadataDao]) -> ['Metadata']:
        return [cls.from_metadata_dao(metadata_dao) for metadata_dao in metadata_daos]

    def to_dao(self) -> MetadataDao:
        return MetadataDao(metadata_id=self._id, key=self.key, value=self.value)

    @staticmethod
    def to_metadata_daos(metadata: ['Metadata']) -> [MetadataDao]:
        return [metadata.to_dao() for metadata in metadata]
