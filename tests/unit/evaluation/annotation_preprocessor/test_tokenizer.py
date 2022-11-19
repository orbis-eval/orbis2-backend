from orbis2.evaluation.annotation_preprocessor.tokenizer import AnnotationTokenizer, TokenizeBy
from orbis2.model.annotation import get_mock_annotation as a


def test_tokenize_whitespace_tokenization():
    """
    Test tokenization of surface forms by splitting them based on the whitespaces between them.
    """
    annotations = [a(10, 38, 'Grosser Gott wir loben dich!'),
                   a(40, 70, 'Herr, wir rühmen deine Stärke!')]
    tokenized = AnnotationTokenizer(tokenize_by=TokenizeBy.WHITESPACE).preprocess(annotations)

    assert tokenized == [a(10, 17, 'Grosser'),
                         a(18, 22, 'Gott'),
                         a(23, 26, 'wir'),
                         a(27, 32, 'loben'),
                         a(33, 38, 'dich!'),
                         a(40, 45, 'Herr,'),
                         a(46, 49, 'wir'),
                         a(50, 56, 'rühmen'),
                         a(57, 62, 'deine'),
                         a(63, 70, 'Stärke!')]


def test_tokenize_character_tokenization():
    """
    Test tokenization into single characters.
    """
    annotations = [a(10, 38, 'Grosser Gott wir loben dich!'),
                   a(40, 70, 'Herr, wir rühmen deine Stärke!')]
    tokenized = AnnotationTokenizer(tokenize_by=TokenizeBy.CHARACTERS).preprocess(annotations)
    for annotation in annotations:
        for start_pos, surface_form in enumerate(annotation.surface_forms[0], start=annotation.start_indices[0]):
            assert a(start_pos, start_pos + 1, surface_form) == tokenized.pop(0)

    assert len(tokenized) == 0
