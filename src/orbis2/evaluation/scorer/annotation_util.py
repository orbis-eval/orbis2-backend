from orbis2.model.annotation import Annotation


def overlap(true, predicted):
    """
    Compute whether two Annotations overlap.

    Return:
        True if predicted overlaps true.
    """
    return predicted.end >= true.start and predicted.start <= true.end


if __name__ == '__main__':

    def test_overlap():
        true = Annotation(10, 20)
        perfect = Annotation(10, 20)
        none = Annotation(5, 9)
        none2 = Annotation(21, 25)
        larger = Annotation(9, 21)
        left = Annotation(5, 11)
        right = Annotation(19, 22)

        assert overlap(true, perfect)
        assert overlap(true, larger)
        assert overlap(true, left)
        assert overlap(true, right)
        assert overlap(larger, true)
        assert overlap(left, true)
        assert overlap(right, true)

        assert not overlap(true, none)
        assert not overlap(true, none2)
        assert not overlap(none, true)
        assert not overlap(none2, true)


    test_overlap()