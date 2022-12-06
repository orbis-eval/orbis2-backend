from abc import abstractmethod


class BaseModel:

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @property
    def id(self) -> int:
        """

        Returns: the ID of the current object, which is defined by its hash.
        """
        return self.__hash__()
