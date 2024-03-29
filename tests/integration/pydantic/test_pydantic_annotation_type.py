from xxhash import xxh32_intdigest

from orbis2.model.annotation_type import AnnotationType
from orbis2.model.corpus import Corpus


def test_annotation_type_initialization():
    """
    Tests, whether Annotation Types are correctly initialized.
    """
    a = AnnotationType(name='annotation_type_1')
    print(a.dict())
    assert a.dict() == {'name': 'annotation_type_1',
                        'color_id': None,
                        '_id': xxh32_intdigest('annotation_type_1')}


def test_annotation_type_pydantic_model():
    """
    Ensure that the AnnotationType pydantic model is serializable.
    """
    corpus = Corpus(
        name='corpus1',
        supported_annotation_types=[
            AnnotationType(name='annotation-type1', color_id=0),
            AnnotationType(name='annotation-type2', color_id=1)
        ],
    )

    assert corpus.json()
