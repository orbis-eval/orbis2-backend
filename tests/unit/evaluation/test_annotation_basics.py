from orbis2.model.annotation import get_mock_annotation as Annotation


# noinspection PyPep8Naming
def test_eq_twoAnnotations_returnsTrue():
    a1 = Annotation(3, 8)
    b1 = Annotation(3, 8)
    assert a1 == b1


# noinspection PyPep8Naming
def test_eq_twoAnnotations_returnsFalse():
    a1 = Annotation(3, 8)
    a2 = Annotation(7, 9)
    assert a1 != a2


# noinspection PyPep8Naming
def test_eq_twoMultiSurfaceFormAnnotations_returnsTrue():
    a1 = Annotation((3, 20, 25), (12, 23, 27))
    a2 = Annotation((3, 20, 25), (12, 23, 27))
    assert a1 == a2


# noinspection PyPep8Naming
def test_eq_twoMultiSurfaceFormAnnotations_returnsFalse():
    a1 = Annotation((3, 20, 25), (12, 23, 27))
    a3 = Annotation((3, 20, 25, 30), (12, 23, 27, 32))
    a4 = Annotation((3, 20, 25), (12, 24, 27))
    assert a1 != a3
    assert a1 != a4


def test_in_annotation_returnsTrue():
    a1 = Annotation(3, 8)
    annotation_list = [Annotation(3, 8), Annotation(3, 8)]
    assert a1 in annotation_list
    assert annotation_list.count(a1) == 2


def test_in_annotation_returnsFalse():
    annotation_list = [Annotation(3, 8), Annotation(3, 8)]
    assert Annotation(7, 9) not in annotation_list


def test_len_annotation_returnsSameNumber():
    assert len(Annotation(3, 8)) == 5
    assert len(Annotation((3, 10, 22), (8, 15, 24))) == 5 + 5 + 2
