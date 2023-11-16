from abc import abstractmethod
from copy import deepcopy
from typing import Dict

from pydantic import BaseModel


class OrbisPydanticBaseModel(BaseModel):

    class Config:
        allow_population_by_field_name = True

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @property
    def identifier(self) -> int:
        """
        Returns: the ID of the current object, which is defined by its hash.
            The underscore is necessary, otherwise the deserialization of the property throws an error.
        """
        return self.__hash__()

    def refined_copy(self, **kwargs):
        """
        Return:
            A deep copy of the given object with provided key value pairs modified.
        """
        copy = deepcopy(self)
        return copy.set(**kwargs)

    def set(self, **kwargs) -> 'OrbisPydanticBaseModel':    # noqa A003
        """
        Set the given keys to the provided values for the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def dict(self, *args, **kwargs):                        # noqa A003
        output = super().dict(*args, **kwargs)
        output['identifier'] = self.identifier
        return output

    @classmethod
    def delete_id_fields(cls, d: Dict) -> Dict:
        """
        Delete the `_id` fields from the json output.

        Note: required for unit testing.
        """
        if isinstance(d, dict):
            return {k: cls.delete_id_fields(v) for k, v in d.items() if k != '_id'}
        elif isinstance(d, list):
            return [cls.delete_id_fields(item) for item in d]
        else:
            return d

    def __str__(self):
        attr_values = [f'{key}={value}'
                       for key, value in sorted(self.dict().items()) if key != '_id'] + [f'_id={self.identifier}']
        return f'<{self.__class__.__name__}({", ".join(attr_values)})>'

    def __repr__(self):
        return self.__str__()
