from orbis2.database.orbis.entities.metadata_dao import MetadataDao


class Metadata:

    def __init__(self, key: str, value: str):
        """
        CONSTRUCTOR

        """
        self.metadata_id = None
        self.key = key
        self.value = value

    @classmethod
    def from_metadata_dao(cls, metadata_dao: MetadataDao) -> 'Metadata':
        metadata = cls(metadata_dao.key, metadata_dao.value)
        metadata.metadata_id = metadata_dao.metadata_id
        return metadata

    @classmethod
    def from_metadata_daos(cls, metadata_daos: [MetadataDao]) -> ['Metadata']:
        return [Metadata.from_metadata_dao(metadata_dao) for metadata_dao in metadata_daos]

    def to_dao(self) -> MetadataDao:
        return MetadataDao(metadata_id=self.metadata_id, key=self.key, value=self.value)

    @staticmethod
    def to_metadata_daos(metadata: ['Metadata']) -> [MetadataDao]:
        return [metadata.to_dao() for metadata in metadata]
