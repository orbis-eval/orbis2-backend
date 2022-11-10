from typing import Tuple, Union


class Annotation:
    """
    Mock Annotation class used within the unittests.
    """

    def __init__(self, start: Union[Tuple[int, ...], int],
                 end: Union[Tuple[int, ...], int]):
        if isinstance(start, int):
            start = (start,)
        if isinstance(end, int):
            end = (end,)

        self.start = start
        self.end = end

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
