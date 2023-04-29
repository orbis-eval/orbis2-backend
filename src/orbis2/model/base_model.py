from abc import abstractmethod
from pydantic import BaseModel


class OrbisPydanticBaseModel(BaseModel):

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @property
    def _id(self) -> int:
        """
        Returns: the ID of the current object, which is defined by its hash.
            The underscore is necessary, otherwise the deserialization of the property throws an error.
        """
        return self.__hash__()

    def dict(self, *args, **kwargs):
        output = super().dict(*args, **kwargs)
        output['_id'] = self._id
        return output
