from orbis2.model.annotation import Annotation


def test_equality():
    a1 = Annotation(3, 8)
    a2 = Annotation(7, 9)
    b1 = Annotation(3, 8)

    assert a1 != a2
    assert a1 == b1


def test_multi_surface_form_equality():
    a1 = Annotation(start=(3, 20, 25), end=(12, 23, 27))
    a2 = Annotation(start=(3, 20, 25), end=(12, 23, 27))
    a3 = Annotation(start=(3, 20, 25, 30), end=(12, 23, 27, 32))
    a4 = Annotation(start=(3, 20, 25), end=(12, 24, 27))

    assert a1 == a2
    assert a1 != a3
    assert a1 != a4


def test_in():
    a1 = Annotation(3, 8)
    a2 = Annotation(7, 9)
    annotation_list = [Annotation(3, 8), Annotation(3, 8)]
    assert a1 in annotation_list
    assert a2 not in annotation_list
    assert annotation_list.count(a1) == 2


def test_len():
    assert len(Annotation(3, 8)) == 5
    assert len(Annotation((3, 10, 22), (8, 15, 24))) == 5 + 5 + 2
