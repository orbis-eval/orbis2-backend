

class BaseModel:

    def get_id(self) -> int:
        """

        Returns: the ID of the current object, which is defined by its hash.
        """
        return self.__hash__()
