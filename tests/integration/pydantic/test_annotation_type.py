from orbis2.model.annotation_type import AnnotationType
from orbis2.model.corpus import Corpus


def test_annotation_type_initialization():
    """
    Tests, whether Annotation Types are correctly initialized.
    """
    a = AnnotationType(name='annotation_type_1')
    assert a.dict()


def test_annotation_type_pydantic_model():
    """
    Ensure that the AnnotationType pydantic model is serializable.
    """
    corpus = Corpus(
        name='corpus1',
        supported_annotation_types={
            AnnotationType(name='annotation-type1'): 0,
            AnnotationType(name='annotation-type2'): 1
        },
    )

    assert corpus.dict()