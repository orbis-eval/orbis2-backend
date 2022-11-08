class Annotation:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __gt__(self, other):
        return self.start >= other.start and self.end >= other.end

    def __lt__(self, other):
        return not self.__gt__(other)

    def __hash__(self):
        return self.start + 1048576 * self.end