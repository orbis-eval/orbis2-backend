from typing import List


class AbstractSurfaceMatcher:

    def score(self, true_annotations: List, predicted_annotations: List) -> \
            List:
        # TODO: correctly align annotations prior to scoring (!)
        #       and ensure that we do not score annotations multiple times.
        return [self.score_annotation(true, predicted)
                for true, predicted in zip(true_annotations, predicted_annotations)]

    @staticmethod
    def overlap(true, predicted):
        """
        Return:
            True if predicted overlaps true.
        """
        return predicted.end >= true.start and predicted.start <= true.end

    def score_annotation(self, true, predicted):
        """
        Args:
            true: the gold standard, true annotation
            predicted: the predicted annotations
        """
        raise NotImplementedError


class PerfectMatcher(AbstractSurfaceMatcher):

    def score_annotation(self, true, predicted):
        return 1 if true.start == predicted.start and true.end == true.end \
            else 0


class OverlappingMatcher(AbstractSurfaceMatcher):

    def score_annotation(self, true, predicted):
        return 1 if self.overlap(true, predicted) else 0



#
# Unittests
#
if __name__ == '__main__':

    class Annotation:

        def __init__(self, start, end):
            self.start = start
            self.end = end

    def test_overlap():
        true = Annotation(10, 20)
        perfect = Annotation(10, 20)
        none = Annotation(5, 9)
        none2 = Annotation(21, 25)
        larger = Annotation(9, 21)
        left = Annotation(5, 11)
        right = Annotation(19, 22)

        assert AbstractSurfaceMatcher.overlap(true, perfect)
        assert AbstractSurfaceMatcher.overlap(true, larger)
        assert AbstractSurfaceMatcher.overlap(true, left)
        assert AbstractSurfaceMatcher.overlap(true, right)
        assert AbstractSurfaceMatcher.overlap(larger, true)
        assert AbstractSurfaceMatcher.overlap(left, true)
        assert AbstractSurfaceMatcher.overlap(right, true)

        assert not AbstractSurfaceMatcher.overlap(true, none)
        assert not AbstractSurfaceMatcher.overlap(true, none2)
        assert not AbstractSurfaceMatcher.overlap(none, true)
        assert not AbstractSurfaceMatcher.overlap(none2, true)


    test_overlap()