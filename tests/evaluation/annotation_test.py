from orbis2.model.annotation import Annotation


def test_equality():
    a1 = Annotation(3, 8)
    a2 = Annotation(7, 9)
    b1 = Annotation(3, 8)

    assert a1 != a2
    assert a1 == b1


def test_in():
    a1 = Annotation(3, 8)
    a2 = Annotation(7, 9)
    l = [Annotation(3, 8), Annotation(3, 8)]
    assert a1 in l
    assert a2 not in l
    assert l.count(a1) == 2
