from abc import ABC, abstractmethod


class BaseImporter(ABC):
    @abstractmethod
    def validate(self, file):
        pass

    @abstractmethod
    def get_annotated_documents(self, file):
        pass

    @abstractmethod
    def get_annotation_types(self, file):
        pass
